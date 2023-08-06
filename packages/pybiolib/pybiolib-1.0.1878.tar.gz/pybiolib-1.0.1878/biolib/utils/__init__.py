import io
import collections
import multiprocessing
import os
import time
import sys
from urllib.parse import urlparse

import requests
from importlib_metadata import version, PackageNotFoundError

# try fetching version, if it fails (usually when in dev), add default
from biolib.biolib_errors import BioLibError
from biolib.biolib_logging import logger_no_user_data
from biolib.typing_utils import Tuple, Iterator
from .multipart_uploader import MultiPartUploader, get_chunk_iterator_from_bytes

try:
    BIOLIB_PACKAGE_VERSION = version('pybiolib')
except PackageNotFoundError:
    BIOLIB_PACKAGE_VERSION = '0.0.0'

IS_DEV = os.getenv('BIOLIB_DEV', '').upper() == 'TRUE'

BIOLIB_BASE_URL = os.getenv('BIOLIB_BASE_URL', default='https://biolib.com').lower()

BIOLIB_CLOUD_BASE_URL = os.getenv('BIOLIB_CLOUD_BASE_URL', '').lower()

BIOLIB_PACKAGE_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BIOLIB_CLOUD_ENVIRONMENT = os.getenv('BIOLIB_CLOUD_ENVIRONMENT', '').lower()

BIOLIB_IS_RUNNING_IN_ENCLAVE = BIOLIB_CLOUD_ENVIRONMENT == 'enclave'

IS_RUNNING_IN_CLOUD = BIOLIB_CLOUD_ENVIRONMENT in ('enclave', 'non-enclave')

DISABLE_CLIENT_SIDE_ENCRYPTION = os.getenv('BIOLIB_DISABLE_CLIENT_SIDE_ENCRYPTION', '').upper() == 'TRUE'

BASE_URL_IS_PUBLIC_BIOLIB = BIOLIB_BASE_URL.endswith('biolib.com') or \
                            os.environ.get('BIOLIB_ENVIRONMENT_IS_PUBLIC_BIOLIB', '').upper() == 'TRUE'

# sys.stdout is an instance of OutStream in Jupyter and Colab which does not have .buffer
if not hasattr(sys.stdout, 'buffer'):
    IS_RUNNING_IN_NOTEBOOK = True
else:
    IS_RUNNING_IN_NOTEBOOK = False

STREAM_STDOUT = False

if BIOLIB_CLOUD_ENVIRONMENT and not IS_RUNNING_IN_CLOUD:
    logger_no_user_data.warning((
        'BIOLIB_CLOUD_ENVIRONMENT defined but does not specify the cloud environment correctly. ',
        'The compute node will not act as a cloud compute node'
    ))

BIOLIB_CLOUD_SKIP_PCR_VERIFICATION = os.getenv('BIOLIB_CLOUD_SKIP_PCR_VERIFICATION', '').upper() == 'TRUE'

BIOLIB_ENABLE_DNS_PROXY = os.getenv('BIOLIB_ENABLE_DNS_PROXY', '').upper() == 'TRUE'

RUN_DEV_JOB_ID = 'run-dev-mocked-job-id'

BIOLIB_FORCE_REMOTE_COMPUTE = os.getenv('BIOLIB_FORCE_REMOTE_COMPUTE', '').upper() == 'TRUE'


def get_absolute_container_image_uri(base_url: str, relative_image_uri: str, job_is_federated: bool = False):
    if base_url == 'https://biolib.com' or job_is_federated:
        container_registry_hostname = 'containers.biolib.com'
    elif base_url in ('https://staging-elb.biolib.com', 'https://staging.biolib.com'):
        container_registry_hostname = 'containers.staging.biolib.com'
    else:
        # Expect registry to be accessible on the hostname of base_url if not running on biolib.com
        base_hostname = urlparse(base_url).hostname
        if not base_hostname:
            raise Exception("Could not get hostname from base_url. Tried to get ecr_proxy_uri for image pulling.")
        container_registry_hostname = base_hostname

    return f'{container_registry_hostname}/{relative_image_uri}'


ByteRangeTuple = Tuple[int, int]
DownloadChunkInputTuple = Tuple[ByteRangeTuple, str]


def _download_chunk(input_tuple: DownloadChunkInputTuple) -> bytes:
    max_download_retries = 10

    byte_range, presigned_url = input_tuple
    start, end = byte_range

    for retry_attempt in range(max_download_retries):
        if retry_attempt > 0:
            logger_no_user_data.debug(f'Attempt number {retry_attempt} for part {start}')
        try:
            response = requests.get(
                url=presigned_url,
                stream=True,
                headers={'range': f'bytes={start}-{end}'},
                timeout=300,  # timeout after 5 min
            )
            if response.ok:
                return_value: bytes = response.raw.data
                logger_no_user_data.debug(f'Returning raw data for part {start}')
                return return_value
            else:
                logger_no_user_data.warning(
                    f'Got not ok response when downloading part {start}:{end}. '
                    f'Got response status {response.status_code} and content: {response.content.decode()} '
                    f'Retrying...'
                )
        except Exception:  # pylint: disable=broad-except
            logger_no_user_data.warning(f'Encountered error when downloading part {start}:{end}. Retrying...')

        time.sleep(5)

    logger_no_user_data.debug(f'Max retries hit, when downloading part {start}:{end}. Exiting...')
    raise BioLibError(f'Max retries hit, when downloading part {start}:{end}. Exiting...')


class ChunkIterator(collections.Iterator):

    def __init__(self, file_size: int, chunk_size: int, presigned_url: str):
        self._semaphore = multiprocessing.BoundedSemaphore(20)  # support 20 chunks to be processed at once
        self._iterator = self._get_chunk_input_iterator(file_size, chunk_size, presigned_url)

    def __iter__(self):
        return self

    def __next__(self):
        if self._semaphore.acquire(timeout=1800):
            return next(self._iterator)
        else:
            raise Exception('Did not receive work within 30 min.')

    def chunk_completed(self) -> None:
        self._semaphore.release()

    @staticmethod
    def _get_chunk_input_iterator(
            file_size: int,
            chunk_size: int,
            presigned_url: str,
    ) -> Iterator[DownloadChunkInputTuple]:
        for index in range(0, file_size, chunk_size):
            byte_range: ByteRangeTuple = (index, index + chunk_size - 1)
            yield byte_range, presigned_url


def download_presigned_s3_url(presigned_url: str, output_file_path: str) -> None:
    chunk_size = 50_000_000

    with requests.get(presigned_url, stream=True, headers={'range': 'bytes=0-1'}) as response:
        if not response.ok:
            raise Exception(f'Got response status code {response.status_code} and content {response.content.decode()}')

        file_size = int(response.headers['Content-Range'].split('/')[1])

    chunk_iterator = ChunkIterator(file_size, chunk_size, presigned_url)

    bytes_written = 0
    # use 16 cores, unless less is available
    process_pool = multiprocessing.Pool(processes=min(16, multiprocessing.cpu_count() - 1))
    try:
        with open(output_file_path, 'ab') as output_file:
            for index, data in enumerate(process_pool.imap(_download_chunk, chunk_iterator)):
                logger_no_user_data.debug(f'Writing part {index} to file...')
                output_file.write(data)

                bytes_written += chunk_size
                approx_progress_percent = min(bytes_written / file_size * 100, 100)
                logger_no_user_data.debug(
                    f'Wrote part {index} of {file_size} to file, '
                    f'the approximate progress is {round(approx_progress_percent, 2)}%'
                )
                chunk_iterator.chunk_completed()
    finally:
        process_pool.close()


def stream_process_output(proc) -> None:
    while proc.poll() is None:
        stdout = io.TextIOWrapper(proc.stdout, newline='')
        stderr = io.TextIOWrapper(proc.stderr, newline='')
        try:
            for line in stdout:
                sys.stdout.write(line)

            for line in stderr:
                sys.stderr.write(line)
        except Exception as error:  # pylint: disable=broad-except
            logger_no_user_data.debug(f'Got an error while streaming process output: {error}')
