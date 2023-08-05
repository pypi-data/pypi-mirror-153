import requests

from biolib.biolib_api_client.auth import BearerAuth
from biolib.biolib_api_client import BiolibApiClient
from biolib.biolib_api_client.lfs_types import LargeFileSystemVersion, LargeFileSystem, ZipProxyFileListResponse
from biolib.biolib_errors import BioLibError


class BiolibLargeFileSystemApi:

    @staticmethod
    def create(account_uuid: str, name: str) -> LargeFileSystem:
        response = requests.post(
            f'{BiolibApiClient.get().base_url}/api/lfs/',
            auth=BearerAuth(BiolibApiClient.get().access_token),
            timeout=5,
            json={'account_uuid': account_uuid, 'name': name}
        )

        if not response.ok:
            raise BioLibError(response.content.decode())

        lfs: LargeFileSystem = response.json()
        return lfs

    @staticmethod
    def fetch_version(lfs_version_uuid: str) -> LargeFileSystemVersion:
        response = requests.get(
            f'{BiolibApiClient.get().base_url}/api/lfs/versions/{lfs_version_uuid}/',
            auth=BearerAuth(BiolibApiClient.get().access_token),
            timeout=5,
        )

        if not response.ok:
            raise BioLibError(response.content.decode())

        lfs_version: LargeFileSystemVersion = response.json()
        return lfs_version

    @staticmethod
    def fetch_file_list(presigned_download_url: str) -> ZipProxyFileListResponse:
        base_url = BiolibApiClient.get().base_url
        if base_url == 'https://biolib.com':
            source_file_proxy_url = 'https://blbcdn.com/source-file-proxy'
        elif base_url == 'https://staging.biolib.com':
            source_file_proxy_url = 'https://staging.blbcdn.com/source-file-proxy'
        else:
            source_file_proxy_url = f'{base_url}/source-file-proxy'

        response = requests.post(
            f'{source_file_proxy_url}/files/',
            timeout=10,
            json={'zip_url': presigned_download_url},
        )

        if not response.ok:
            raise BioLibError(response.content.decode())

        response_dict: ZipProxyFileListResponse = response.json()
        return response_dict

    @staticmethod
    def create_version(resource_uuid: str) -> LargeFileSystemVersion:
        response = requests.post(
            f'{BiolibApiClient.get().base_url}/api/lfs/versions/',
            auth=BearerAuth(BiolibApiClient.get().access_token),
            json={'resource_uuid': resource_uuid},
            timeout=5,
        )

        if not response.ok:
            raise BioLibError(response.content.decode())

        lfs_version: LargeFileSystemVersion = response.json()
        return lfs_version
