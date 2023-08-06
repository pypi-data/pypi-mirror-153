from abc import ABC, abstractmethod

import requests

from biolib.typing_utils import Iterable


class IndexableBuffer(ABC):

    def __init__(self):
        self.pointer = 0

    @abstractmethod
    def get_data(self, start: int, length: int) -> bytes:
        pass

    @abstractmethod
    def get_data_as_iterable(self, start: int, length: int, chunk_size: int) -> Iterable[bytes]:
        pass

    def get_data_as_string(self, start: int, length: int) -> str:
        return self.get_data(start=start, length=length).decode()

    def get_data_as_int(self, start: int, length: int) -> int:
        return int.from_bytes(bytes=self.get_data(start=start, length=length), byteorder='big')

    def get_data_with_pointer(self, length: int) -> bytes:
        data = self.get_data(start=self.pointer, length=length)
        self.pointer += length
        return data

    def get_data_with_pointer_as_int(self, length: int) -> int:
        data = self.get_data_as_int(start=self.pointer, length=length)
        self.pointer += length
        return data

    def get_data_with_pointer_as_string(self, length: int) -> str:
        data = self.get_data_as_string(start=self.pointer, length=length)
        self.pointer += length
        return data


class RemoteIndexableBuffer(IndexableBuffer):

    def __init__(self, url: str):
        super().__init__()
        self._url = url

    def get_data(self, start: int, length: int) -> bytes:
        if length < 0:
            raise Exception('get_data length must be positive')

        if length == 0:
            return bytes(0)

        end = start + length - 1
        response = requests.get(url=self._url, headers={'range': f'bytes={start}-{end}'})
        if not response.ok:
            raise Exception(f'get_data got not ok response status {response.status_code}')

        data: bytes = response.content
        if len(data) != length:
            raise Exception(f'get_data got response of unexpected length. Got {len(data)} expected {length}.')

        return data

    def get_data_as_iterable(self, start: int, length: int, chunk_size: int) -> Iterable[bytes]:
        if length < 0:
            raise Exception('get_data length must be positive')

        if length == 0:
            return []

        end = start + length - 1
        response = requests.get(
            url=self._url,
            headers={'range': f'bytes={start}-{end}'},
            stream=True,
            timeout=60,
        )
        return response.iter_content(chunk_size=chunk_size)


class InMemoryIndexableBuffer(IndexableBuffer):

    def __init__(self, data: bytes):
        super().__init__()
        self._buffer = data
        self._length_bytes = len(data)

    def get_data(self, start: int, length: int) -> bytes:
        end = start + length
        return self._buffer[start:end]

    def get_data_as_iterable(self, start: int, length: int, chunk_size: int) -> Iterable[bytes]:
        raise NotImplementedError

    def __len__(self):
        return self._length_bytes


class LazyLoadedFile:

    def __init__(self, path: str, buffer: IndexableBuffer, start: int, length: int):
        self._path = path
        self._buffer = buffer
        self._start = start
        self._length = length

    @property
    def path(self) -> str:
        return self._path

    def get_data(self) -> bytes:
        return self._buffer.get_data(start=self._start, length=self._length)

    def get_data_as_iterable(self) -> Iterable[bytes]:
        return self._buffer.get_data_as_iterable(start=self._start, length=self._length, chunk_size=1_000_000)
