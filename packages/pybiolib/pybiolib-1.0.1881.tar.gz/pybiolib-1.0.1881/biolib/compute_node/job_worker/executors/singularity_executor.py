import glob
import shutil
import time
import zipfile
import os
import io
import shlex

from spython.main import Client # type: ignore
from spython.instance import Instance # type: ignore

from biolib import utils
from biolib.biolib_binary_format import ModuleOutput, ModuleInput
from biolib.biolib_singularity_client import BiolibSingularityClient
from biolib.biolib_logging import logger
from biolib.compute_node import utils as compute_node_utils
from biolib.compute_node.job_worker.executors.base_executor import BaseExecutor
from biolib.compute_node.job_worker.executors.types import StatusUpdate, LocalExecutorOptions
from biolib.compute_node.job_worker.mappings import Mappings, path_without_first_folder
from biolib.compute_node.job_worker.utils import ComputeProcessException
from biolib.compute_node.utils import SystemExceptionCodes
from biolib.typing_utils import List, Optional
from biolib.utils import get_absolute_container_image_uri


class SingularityExecutor(BaseExecutor):

    def __init__(self, options: LocalExecutorOptions):
        super().__init__(options)

        # Move this to shared class
        ##########
        if self._options['root_job_id'] == utils.RUN_DEV_JOB_ID:
            self._image_uri = self._options['module']['image_uri']
        else:
            self._image_uri = get_absolute_container_image_uri(
                base_url=self._options['biolib_base_url'],
                relative_image_uri=self._options['module']['image_uri'],
                job_is_federated=True if self._options['job'].get('federated_job_uuid') else False
            )

        self._send_system_exception = options['send_system_exception']
        self._send_stdout_and_stderr = options['send_stdout_and_stderr']

        federated_job_uuid: Optional[str] = self._options['job'].get('federated_job_uuid')
        if options['compute_node_info'] is not None and not federated_job_uuid:
            compute_node_public_id = options['compute_node_info']['public_id']
            compute_node_auth_token = options['compute_node_info']['auth_token']
            # Use "|" to separate the fields as this makes it easy for the ECR proxy to split
            ecr_proxy_auth_token = f'cloud-{compute_node_public_id}|{compute_node_auth_token}'
        else:
            ecr_proxy_auth_token = options['access_token']

        docker_auth_job_id = federated_job_uuid or self._options['job']['public_id']
        self._docker_auth_config = {'username': 'AWS', 'password': f'{ecr_proxy_auth_token},{docker_auth_job_id}'}
        self._random_docker_id = compute_node_utils.random_string(15)
        self._compute_process_dir = os.path.dirname(os.path.realpath(__file__))
        #########

        self._instance: Optional[Instance] = None
        self._input_files_dir = SingularityExecutor._create_dir_and_return_path(
            f'.biolib_singularity/biolib_input_{self._random_docker_id}'
        )
        self._runtime_files_dir = SingularityExecutor._create_dir_and_return_path(
            f'.biolib_singularity/biolib_runtime_{self._random_docker_id}'
        )
        self._output_files_dir = SingularityExecutor._create_dir_and_return_path(
            f'.biolib_singularity/biolib_output_{self._random_docker_id}'
        )
        self._pull_folder = SingularityExecutor._create_dir_and_return_path(
            '.biolib_singularity/images'
        )

        # The image file name is without the registry domain `containers.biolib.com/`
        self._image_file_name = f'{self._image_uri.split("/", 1)[1]}.sif'
        self._singularity_options: List[str] = []

        self._input_binds: List['str'] = []
        self._runtime_binds: List['str'] = []

        self._spython_client = BiolibSingularityClient.get_singularity_client()

    @staticmethod
    def _create_dir_and_return_path(path):
        os.makedirs(path, exist_ok=True)
        return path

    # Move this to shared class
    #############
    def execute_module(self, module_input_serialized: bytes) -> bytes:
        send_status_update = self._options['send_status_update']
        send_system_exception = self._options['send_system_exception']

        module_input = ModuleInput(module_input_serialized).deserialize()

        # TODO: fix these status updates such that they also make sense for run-dev
        send_status_update(StatusUpdate(progress=55, log_message='Pulling images...'))

        self._pull()

        send_status_update(StatusUpdate(progress=70, log_message='Computing...'))
        start_time = time.time()

        stdout, stderr, exit_code, mapped_output_files = self._execute_helper(module_input)

        try:
            module_output_serialized: bytes = ModuleOutput().serialize(stdout, stderr, exit_code, mapped_output_files)
            logger.debug(f'Compute time: {time.time() - start_time}')
            return module_output_serialized

        except Exception as exception:
            raise ComputeProcessException(
                exception,
                SystemExceptionCodes.FAILED_TO_SERIALIZE_AND_SEND_MODULE_OUTPUT.value,
                send_system_exception
            ) from exception
        finally:
            try:
                self.cleanup()
            except Exception:  # pylint: disable=broad-except
                logger.error('SingularityExecutor failed to clean up container')
    #############

    def _pull(self):
        try:
            # Don't pull if SIF already exists
            if os.path.exists(self._image_file_name):
                return

            start_time = time.time()
            os.environ['SINGULARITY_DOCKER_USERNAME'] = self._docker_auth_config['username']
            os.environ['SINGULARITY_DOCKER_PASSWORD'] = self._docker_auth_config['password']
            self._spython_client.pull(
                image=f'docker://{self._image_uri}',
                pull_folder=self._pull_folder
            )
            logger.debug(f'Pulled image in: {time.time() - start_time}')

        except Exception as exception:
            raise ComputeProcessException(
                exception,
                SystemExceptionCodes.FAILED_TO_PULL_DOCKER_IMAGE.value,
                self._send_system_exception,
                may_contain_user_data=False
            ) from exception

    def _execute_helper(self, module_input):
        runtime_files = {}
        if self._options['runtime_zip_bytes']:
            runtime_files = self.get_runtime_files(self._options['runtime_zip_bytes'])
            self._runtime_binds = SingularityExecutor.populate_bind_mount_dir(
                mappings=self._options['module']['source_files_mappings'],
                bind_dir=self._runtime_files_dir,
                arguments=module_input['arguments'],
                files=runtime_files
            )

        self._input_binds = SingularityExecutor.populate_bind_mount_dir(
            mappings=self._options['module']['input_files_mappings'],
            bind_dir=self._input_files_dir,
            arguments=module_input['arguments'],
            files=module_input['files']
        )

        try:
            # Set network to None to disable networking in container
            self._singularity_options = [
                '--net',
                '--network',
                'none',
                '--writable',
                *self._input_binds,
                *self._runtime_binds,
                '--bind',
                f'{self._output_files_dir}:/output',
            ]

            self._instance = self._spython_client.instance(
                image=f'{self._pull_folder}/{self._image_file_name}',
                options=self._singularity_options,
                start=True
            )

            logger.debug('Running Singularity container')
            result = Client.run(
                image=self._instance,
                args=shlex.split(self._options['module']['command']) + module_input['arguments'],
                contain=True,
                nv=False,  # TODO: Set to true when GPUs are needed
                stream=False,  # TODO: Set to true to test output streaming
                return_result=True
            )

            exit_code = result['return_code']
            # 137 is the error code from linux OOM killer (Should catch 90% of OOM errors)
            if exit_code == 137:
                raise ComputeProcessException(
                    MemoryError(),
                    SystemExceptionCodes.OUT_OF_MEMORY.value,
                    self._send_system_exception
                )

            logger.debug(f'Singularity container exited with code {exit_code}')

            full_stdout = result['message'].encode()
            full_stderr = b''  # TODO: Figure out a way to get STDERR from singularity

            mapped_output_files = self._get_output_files(arguments=module_input['arguments'])
            return full_stdout, full_stderr, exit_code, mapped_output_files

        except Exception as exception:
            raise ComputeProcessException(
                exception,
                SystemExceptionCodes.FAILED_TO_RUN_COMPUTE_CONTAINER.value,
                self._send_system_exception
            ) from exception

    def cleanup(self):
        # Don't clean up if already in the process of doing so, or done doing so
        if self._is_cleaning_up:
            return
        else:
            self._is_cleaning_up = True

        bind_dir_time = time.time()
        for path_to_delete in [self._input_files_dir, self._runtime_files_dir, self._output_files_dir]:
            if os.path.exists(path_to_delete):
                shutil.rmtree(path_to_delete)
        logger.debug(f"Deleted bind dirs in: {time.time() - bind_dir_time}")

        instance_time = time.time()
        if self._instance:
            try:
                self._instance.stop(timeout=0)
            except Exception:  # pylint: disable=broad-except
                logger.debug('Instance could not be stopped or is already stopped')
        logger.debug(f"Deleted compute instance in: {time.time() - instance_time}")


    @staticmethod
    def populate_bind_mount_dir(mappings, bind_dir, arguments: List[str], files):
        mappings = Mappings(mappings, arguments)
        bind_mounts = []
        for path, data in files.items():
            # Skip the empty root entry that occurs in the runtime zip
            if path == '/':
                continue

            # Make all paths absolute
            if not path.startswith('/'):
                path = '/' + path

            mapped_file_names = mappings.get_mappings_for_path(path)
            for mapped_file_name in mapped_file_names:
                host_path = f'{bind_dir}{path}'
                if path.endswith('/'):
                    os.makedirs(host_path, exist_ok=True)
                else:
                    open(host_path, 'wb').write(data)
                bind_mounts.extend(['--bind', f'{host_path}:{mapped_file_name}'])
        return bind_mounts

    def get_runtime_files(self, runtime_zip_data, remove_root_folder=True):
        runtime_zip = zipfile.ZipFile(io.BytesIO(runtime_zip_data))
        runtime_files = {}
        for zip_file_name in runtime_zip.namelist():
            # Make paths absolute and remove root folder from path
            if remove_root_folder:
                file_path = '/' + path_without_first_folder(zip_file_name)
            else:
                file_path = '/' + zip_file_name

            runtime_files[file_path] = runtime_zip.read(zip_file_name)
        return runtime_files

    def _get_output_files(self, arguments: List[str]):
        module = self._options['module']
        mapped_output_files = {}

        try:
            # Write list of output files to retrieve
            files_to_get = [mapping['from_path'] for mapping in module['output_files_mappings']]
            with open(f'{self._output_files_dir}/filelist.txt', 'w') as file:
                for file_path in files_to_get:
                    file.write(f'{file_path}\n')

            bash_script = """
            #!/bin/sh
            cat /output/filelist.txt | while read line 
            do
                echo $line
                cp -r $line /output
            done
            """

            with open(f'{self._output_files_dir}/output_retriever.sh', 'w') as file:
                file.write(bash_script)

            Client.run(
                image=self._instance,
                args=['/bin/sh', '-c', 'chmod +x /output/output_retriever.sh && /output/output_retriever.sh'],
                options=self._singularity_options,
                contain=True,
            )

            output_mappings = Mappings(module['output_files_mappings'], arguments)
            for original_file_name in glob.iglob(self._output_files_dir + '**/**', recursive=True):
                # Remove the `output_files_dir` folder from file_name
                file_name = original_file_name.replace(self._output_files_dir, '')
                if file_name != '/':
                    mapped_file_names = output_mappings.get_mappings_for_path(file_name)
                    for mapped_file_name in mapped_file_names:
                        mapped_output_files[mapped_file_name] = open(original_file_name, 'rb').read()

        except Exception as exception:
            raise ComputeProcessException(
                exception,
                SystemExceptionCodes.FAILED_TO_RUN_COMPUTE_CONTAINER.value,
                self._send_system_exception
            ) from exception

        return mapped_output_files
