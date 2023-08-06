from biolib.typing_utils import TypedDict


class SimpleFile(TypedDict):
    data: bytes


class FilesInfo(TypedDict):
    path: str
    data_length: int
