import base64
import os
from urllib.parse import urlparse

import requests
from Crypto.Random import get_random_bytes

from biolib import utils
from biolib.biolib_api_client import BiolibApiClient, Job
from biolib.biolib_api_client.biolib_job_api import BiolibJobApi
from biolib.biolib_binary_format.utils import InMemoryIndexableBuffer, RemoteIndexableBuffer
from biolib.biolib_binary_format.encrypted_module_output import EncryptedModuleOutputWithKey
from biolib.biolib_binary_format.unencrypted_module_output import UnencryptedModuleOutput
from biolib.biolib_errors import BioLibError
from biolib.compute_node.cloud_utils import CloudUtils
from biolib.compute_node.job_worker.job_key_cache import JobKeyCacheState
from biolib.biolib_logging import logger_no_user_data, logger


class JobStorage:

    @staticmethod
    def upload_module_output(job_uuid: str, module_output: bytes, aes_key_string_b64: str) -> None:
        try:
            if utils.DISABLE_CLIENT_SIDE_ENCRYPTION:
                storage_module_output = UnencryptedModuleOutput.create_from_serialized_module_output(module_output)
                logger_no_user_data.debug(f'Job "{job_uuid}" uploading result to S3...')

            else:
                if not aes_key_string_b64:
                    raise Exception('Missing AES key for module output upload as client side encryption is enabled')
                storage_module_output = EncryptedModuleOutputWithKey(
                    aes_key_string_b64=aes_key_string_b64
                ).create_from_serialized_module_output(module_output)
                logger_no_user_data.debug(f'Job "{job_uuid}" uploading encrypted result to S3...')

        except Exception as error:
            logger_no_user_data.debug('Failed to get storage module output from serialized module output')
            logger.debug(f'Failed to get storage module output from serialized module output due to {error}')
            raise error

        base_url = BiolibApiClient.get().base_url
        config = CloudUtils.get_webserver_config()
        compute_node_auth_token = config['compute_node_info']['auth_token']  # pylint: disable=unsubscriptable-object
        headers = {'Compute-Node-Auth-Token': compute_node_auth_token}

        multipart_uploader = utils.MultiPartUploader(
            start_multipart_upload_request=dict(
                requires_biolib_auth=False,
                url=f'{base_url}/api/jobs/{job_uuid}/storage/results/start_upload/',
                headers=headers,
            ),
            get_presigned_upload_url_request=dict(
                requires_biolib_auth=False,
                url=f'{base_url}/api/jobs/{job_uuid}/storage/results/presigned_upload_url/',
                headers=headers,
            ),
            complete_upload_request=dict(
                requires_biolib_auth=False,
                url=f'{base_url}/api/jobs/{job_uuid}/storage/results/complete_upload/',
                headers=headers,
            ),
        )

        multipart_uploader.upload(
            payload_iterator=utils.get_chunk_iterator_from_bytes(storage_module_output),
            payload_size_in_bytes=len(storage_module_output),
        )

    @staticmethod
    def get_result(job: Job) -> bytes:
        presigned_download_url = BiolibJobApi.get_job_storage_result_download_url(job['auth_token'])

        s3_results_base_url = os.getenv('BIOLIB_CLOUD_RESULTS_BASE_URL', '')
        if s3_results_base_url:
            # Done to hit App Caller Proxy when downloading result from inside an app
            parsed_url = urlparse(presigned_download_url)
            presigned_download_url = f'{s3_results_base_url}{parsed_url.path}?{parsed_url.query}'

        if utils.BASE_URL_IS_PUBLIC_BIOLIB:
            # TODO: Use RemoteIndexableBuffer for EncryptedModuleOutputWithKey
            try:
                result_response = requests.get(
                    url=presigned_download_url,
                    timeout=3600,  # timeout after 1 hour
                )

                if not result_response.ok:
                    raise BioLibError(result_response.content)

            except Exception as error:
                logger.debug(f'Failed to get results from S3 due to {error}')
                raise error

            with JobKeyCacheState() as cache_state:
                aes_key_string_b64 = cache_state[job['public_id']]

            encrypted_module_output = EncryptedModuleOutputWithKey(
                buffer=InMemoryIndexableBuffer(result_response.content),
                aes_key_string_b64=aes_key_string_b64,
            )
            return encrypted_module_output.convert_to_serialized_module_output()

        else:
            buffer = RemoteIndexableBuffer(url=presigned_download_url)
            unencrypted_module_output = UnencryptedModuleOutput(buffer)
            return unencrypted_module_output.convert_to_serialized_module_output()

    @staticmethod
    def generate_and_store_key_buffer_for_job(job_id: str) -> str:
        aes_key_buffer = get_random_bytes(32)
        aes_key_string_b64 = base64.urlsafe_b64encode(aes_key_buffer).decode()

        with JobKeyCacheState() as cache_state:
            cache_state[job_id] = aes_key_string_b64

        return aes_key_string_b64
