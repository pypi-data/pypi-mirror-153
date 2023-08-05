import base64
import random
import sys
import time
import threading
import socket
from queue import Queue

from biolib import utils
from biolib.compute_node.cloud_utils import CloudUtils
from biolib.compute_node.job_worker import JobWorkerProcess
from biolib.compute_node.job_worker.job_storage import JobStorage
from biolib.compute_node.socker_listener_thread import SocketListenerThread
from biolib.compute_node.socket_sender_thread import SocketSenderThread
from biolib.compute_node.webserver import webserver_utils
from biolib.biolib_binary_format import AttestationDocument, SystemStatusUpdate, SystemException
from biolib.compute_node.utils import get_package_type, WorkerThreadException, SystemExceptionCodes
from biolib.biolib_logging import logger, logger_no_user_data

SOCKET_HOST = '127.0.0.1'


class WorkerThread(threading.Thread):
    def __init__(self, compute_state):
        try:
            super().__init__()
            self.compute_state = compute_state
            self._socket_port = random.choice(range(6000, 65000))
            self._socket = None
            self._connection = None
            self._job_worker_process = None
            self._connection_thread = None
            self._listener_thread = None
            self._sender_thread = None
            self._start_and_connect_to_compute_process()

            logger.debug(f"WorkerThread connected to port {self._socket_port}")

        except Exception as exception:
            logger_no_user_data.error(exception)
            raise WorkerThreadException(
                exception,
                SystemExceptionCodes.FAILED_TO_INITIALIZE_WORKER_THREAD.value,
                worker_thread=self,
            ) from exception

    @property
    def _job_uuid(self):
        return self.compute_state['job_id']

    def run(self):
        try:
            while True:
                package = self.compute_state['received_messages_queue'].get()
                if package == b'CANCEL_JOB':
                    logger_no_user_data.info(f'Job "{self._job_uuid}" got cancel signal')
                    self.compute_state['status']['error_code'] = SystemExceptionCodes.CANCELLED_BY_USER.value
                    self.terminate()

                package_type = get_package_type(package)

                if package_type == 'AttestationDocument':
                    self.compute_state['attestation_document'] = AttestationDocument(package).deserialize()

                elif package_type == 'StdoutAndStderr':
                    self.compute_state['status']['stdout_and_stderr_packages_b64'].append(
                        base64.b64encode(package).decode()
                    )

                elif package_type == 'SystemStatusUpdate':
                    progress, log_message = SystemStatusUpdate(package).deserialize()
                    self._set_status_update(progress, log_message)

                elif package_type == 'SystemException':
                    error_code = SystemException(package).deserialize()
                    self.compute_state['status']['error_code'] = error_code
                    logger.debug("Hit error. Terminating Worker Thread and Compute Process")
                    self.compute_state['progress'] = 95
                    self.terminate()

                elif package_type == 'ModuleOutput':
                    self.compute_state['result'] = package

                    if utils.IS_RUNNING_IN_CLOUD:
                        aes_key_string_b64 = self.compute_state.get('aes_key_string_b64')
                        if aes_key_string_b64 or utils.DISABLE_CLIENT_SIDE_ENCRYPTION:
                            logger_no_user_data.debug(f'Job "{self._job_uuid}" uploading result...')
                            JobStorage.upload_module_output(
                                job_uuid=self._job_uuid,
                                module_output=package,
                                aes_key_string_b64=aes_key_string_b64
                            )
                            logger_no_user_data.debug(f'Job "{self._job_uuid}" result uploaded successfully')
                        else:
                            logger_no_user_data.debug("Assuming user will consume result from webserver")

                    self._set_status_update(progress=95, log_message='Result Ready')
                    self.terminate()

                elif package_type == 'AesEncryptedPackage':
                    if self.compute_state['progress'] == 94:  # Check if encrypted package is ModuleOutput
                        self.compute_state['result'] = package
                        self.terminate()
                    else:  # Else it is StdoutAndStderr
                        self.compute_state['status']['stdout_and_stderr_packages_b64'].append(
                            base64.b64encode(package).decode()
                        )

                else:
                    raise Exception(f'Package type from child was not recognized: {package}')

                self.compute_state['received_messages_queue'].task_done()

        except Exception as exception:
            raise WorkerThreadException(
                exception,
                SystemExceptionCodes.FAILED_TO_HANDLE_PACKAGE_IN_WORKER_THREAD.value,
                worker_thread=self,
            ) from exception

    def _set_status_update(self, progress: int, log_message: str) -> None:
        status_update = dict(progress=progress, log_message=log_message)
        logger_no_user_data.debug(f'Job "{self._job_uuid}" got system log: {status_update}')

        self.compute_state['progress'] = progress
        self.compute_state['status']['status_updates'].append(status_update)

    def _start_and_connect_to_compute_process(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger_no_user_data.debug(f'Trying to bind to socket on {SOCKET_HOST}:{self._socket_port}')
        self._socket.bind((SOCKET_HOST, self._socket_port))

        logger_no_user_data.debug(f'Starting to listen to socket on port {self._socket_port}')
        self._socket.listen()
        logger_no_user_data.debug(f'Listening to port {self._socket_port}')

        received_messages_queue = Queue()
        messages_to_send_queue = Queue()

        # Starting a thread for accepting connections before starting the process that should to connect to the socket
        logger_no_user_data.debug('Starting connection thread')
        self._connection_thread = threading.Thread(target=self._accept_new_socket_connection, args=[
            received_messages_queue,
            messages_to_send_queue
        ])
        self._connection_thread.start()
        logger_no_user_data.debug('Started connection thread')
        logger_no_user_data.debug('Starting compute process')

        self._job_worker_process = JobWorkerProcess(socket_port=self._socket_port, log_level=logger.level)
        self._job_worker_process.start()

        self.compute_state['received_messages_queue'] = received_messages_queue
        self.compute_state['messages_to_send_queue'] = messages_to_send_queue
        self.compute_state['worker_thread'] = self

    def _accept_new_socket_connection(self, received_messages_queue, messages_to_send_queue):
        self._connection, _ = self._socket.accept()
        self._listener_thread = SocketListenerThread(self._connection, received_messages_queue)
        self._listener_thread.start()

        self._sender_thread = SocketSenderThread(self._connection, messages_to_send_queue)
        self._sender_thread.start()

    def terminate(self) -> None:
        if self._job_worker_process:
            logger_no_user_data.debug(
                f'Job "{self._job_uuid}" terminating JobWorkerProcess with PID {self._job_worker_process.pid}'
            )
            self._job_worker_process.terminate()

            for _ in range(10):
                if self._job_worker_process.exitcode is not None:
                    logger_no_user_data.debug(
                        f'Job "{self._job_uuid}" worker process exitcode {self._job_worker_process.exitcode}'
                    )
                    break
                else:
                    logger_no_user_data.debug(f'Job "{self._job_uuid}" waiting for worker process to exit...')
                    time.sleep(1)

            if self._job_worker_process.exitcode is None:
                # TODO: Figure out if more error handling is necessary here
                logger_no_user_data.error(f'Job {self._job_uuid} worker process did not exit within 10 seconds')

        if utils.IS_RUNNING_IN_CLOUD:
            # Get and send exception code if present
            system_exception_code = self.compute_state['status'].get('error_code')
            CloudUtils.finish_cloud_job(
                cloud_job_id=self.compute_state['cloud_job_id'],
                system_exception_code=system_exception_code
            )

        if self._socket:
            self._socket.close()

        if self._connection:
            self._connection.close()

        if self.compute_state['progress'] == 95:
            seconds_to_sleep = 60  # 1 minute
            logger_no_user_data.debug(
                f'Job "{self._job_uuid}" worker thread sleeping for {seconds_to_sleep} seconds before cleaning up'
            )
            # sleep to let the user start downloading the result
            time.sleep(seconds_to_sleep)

        if self._job_uuid in webserver_utils.JOB_ID_TO_COMPUTE_STATE_DICT:
            webserver_utils.JOB_ID_TO_COMPUTE_STATE_DICT.pop(self._job_uuid)
            logger_no_user_data.debug(f'Job "{self._job_uuid}" was cleaned up')
        else:
            logger_no_user_data.debug(
                f'Job "{self._job_uuid}" could not be found, maybe it has already been cleaned up'
            )

        logger_no_user_data.debug(f'Job "{self._job_uuid}" worker thread terminated')

        if utils.IS_RUNNING_IN_CLOUD:
            webserver_utils.update_auto_shutdown_time()

        sys.exit()
