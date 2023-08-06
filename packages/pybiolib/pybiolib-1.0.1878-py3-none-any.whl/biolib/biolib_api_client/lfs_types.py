from biolib.typing_utils import TypedDict, List


class LargeFileSystemVersion(TypedDict):
    presigned_download_url: str
    size_bytes: int
    uri: str
    uuid: str


class LargeFileSystem(TypedDict):
    uri: str
    uuid: str


class ZipProxyFileMetadata(TypedDict):
    path: str
    size_bytes: int


class ZipProxyFileListResponse(TypedDict):
    files: List[ZipProxyFileMetadata]


class LargeFileSystemVersionMetadata(LargeFileSystemVersion):
    files: List[ZipProxyFileMetadata]
