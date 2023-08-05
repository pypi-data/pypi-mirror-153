from pathlib import Path
import time
import requests

from biolib.biolib_api_client import BiolibApiClient
from biolib.biolib_api_client.auth import BearerAuth
from biolib.biolib_binary_format import UnencryptedModuleOutput
from biolib.biolib_binary_format.utils import RemoteIndexableBuffer
from biolib.biolib_errors import BioLibError
from biolib.biolib_logging import logger_no_user_data
from biolib.typing_utils import Optional, Dict


class JobResultError(BioLibError):
    pass


class JobResultNotFound(JobResultError):
    pass


class JobResultPermissionError(JobResultError):
    pass


class JobResult:

    def __init__(self, job_uuid: str):
        self._job_uuid = job_uuid

        self._module_output: Optional[UnencryptedModuleOutput] = None

    def save_files(self, output_dir: str) -> None:
        module_output = self._get_module_output()
        output_files = module_output.get_files()
        print(f'Saving {len(output_files)} files to {output_dir}...')

        for file in output_files:
            # Remove leading slash of file_path
            destination_file_path = Path(output_dir) / Path(file.path.lstrip('/'))
            if destination_file_path.exists():
                destination_file_path.rename(f'{destination_file_path}.biolib-renamed.{time.strftime("%Y%m%d%H%M%S")}')

            dir_path = destination_file_path.parent
            if dir_path:
                dir_path.mkdir(parents=True, exist_ok=True)

            with open(destination_file_path, mode='wb') as file_handler:
                for chunk_number, chunk in enumerate(file.get_data_as_iterable()):
                    logger_no_user_data.debug(f'Processing chunk {chunk_number}...')
                    file_handler.write(chunk)

            print(f'  - {destination_file_path}')

        print('\n')

    def _get_presigned_download_url(self) -> str:
        BiolibApiClient.assert_is_signed_in(authenticated_action_description='get result of a job')
        try:
            response = requests.get(
                url=f'{BiolibApiClient.get().base_url}/api/jobs/{self._job_uuid}/storage/results/download/',
                auth=BearerAuth(BiolibApiClient.get().access_token),
            )
            response.raise_for_status()
            response_dict: Dict[str, str] = response.json()
            return response_dict['presigned_download_url']
        except requests.exceptions.HTTPError as error:
            status_code = error.response.status_code

            if status_code == 401:
                raise JobResultPermissionError('You must be signed in to get result of the job') from None
            elif status_code == 403:
                raise JobResultPermissionError(
                    'Cannot get result of job. Maybe the job was created without being signed in?'
                ) from None
            elif status_code == 404:
                raise JobResultNotFound('Job result not found') from None
            else:
                raise JobResultError('Failed to get result of job') from error

        except Exception as error:
            raise JobResultError('Failed to get result of job') from error

    # TODO: Also handle encrypted module output
    def _get_module_output(self) -> UnencryptedModuleOutput:
        if self._module_output is None:
            buffer = RemoteIndexableBuffer(url=self._get_presigned_download_url())
            self._module_output = UnencryptedModuleOutput(buffer)

        return self._module_output
