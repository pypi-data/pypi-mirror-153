from biolib.biolib_binary_format import BioLibBinaryFormatBasePackage
from biolib.biolib_binary_format.utils import IndexableBuffer, InMemoryIndexableBuffer, LazyLoadedFile
from biolib.biolib_binary_format.module_output import ModuleOutput
from biolib.typing_utils import TypedDict, List, Optional, Dict


class Metadata(TypedDict):
    version: int
    type: int
    stdout_length: int
    stderr_length: int
    files_info_length: int
    files_data_length: int
    exit_code: int


class UnencryptedModuleOutput(BioLibBinaryFormatBasePackage):
    _version = 1
    _type = 11
    _metadata_byte_lengths = dict(
        # Note: order is important
        version=1,
        type=1,
        stdout_length=8,
        stderr_length=8,
        files_info_length=8,
        files_data_length=8,
        exit_code=2,
    )
    _metadata_length = sum(_metadata_byte_lengths.values())
    _file_path_length_bytes = 4
    _file_data_length_bytes = 8

    def __init__(self, buffer: IndexableBuffer):
        super().__init__()
        self._buffer = buffer

        self._metadata: Optional[Metadata] = None
        self._stdout: Optional[bytes] = None
        self._stderr: Optional[bytes] = None
        self._files: Optional[List[LazyLoadedFile]] = None

    def get_exit_code(self) -> int:
        metadata = self._get_metadata()
        return metadata['exit_code']

    def get_stdout(self) -> bytes:
        if self._stdout is None:
            metadata = self._get_metadata()
            self._stdout = self._buffer.get_data(start=self._metadata_length, length=metadata['stdout_length'])

        return self._stdout

    def get_stderr(self) -> bytes:
        if self._stderr is None:
            metadata = self._get_metadata()
            self._stderr = self._buffer.get_data(
                start=self._metadata_length + metadata['stdout_length'],
                length=metadata['stderr_length'],
            )

        return self._stderr

    def get_files(self) -> List[LazyLoadedFile]:
        metadata = self._get_metadata()
        if self._files is None:
            self._files = []
            if metadata['files_info_length'] == 0:
                return self._files

            files_info_start = self._metadata_length + metadata['stdout_length'] + metadata['stderr_length']
            files_info_buffer = InMemoryIndexableBuffer(
                data=self._buffer.get_data(start=files_info_start, length=metadata['files_info_length'])
            )

            files_data_pointer = files_info_start + metadata['files_info_length']
            while files_info_buffer.pointer < len(files_info_buffer):
                path_length = files_info_buffer.get_data_with_pointer_as_int(self._file_path_length_bytes)
                path = files_info_buffer.get_data_with_pointer_as_string(path_length)
                data_length = files_info_buffer.get_data_with_pointer_as_int(self._file_data_length_bytes)

                data_start = files_data_pointer
                files_data_pointer += data_length

                self._files.append(LazyLoadedFile(path=path, buffer=self._buffer, start=data_start, length=data_length))

        return self._files

    def _get_metadata(self) -> Metadata:
        if self._metadata is None:
            metadata_buffer = InMemoryIndexableBuffer(self._buffer.get_data(start=0, length=self._metadata_length))

            partial_metadata = {}
            for field_name, field_length in self._metadata_byte_lengths.items():
                value = metadata_buffer.get_data_with_pointer_as_int(length=field_length)  # type: ignore
                if field_name == 'version' and value != UnencryptedModuleOutput._version:
                    raise Exception('Version does not match')

                if field_name == 'type' and value != UnencryptedModuleOutput._type:
                    raise Exception('Type does not match')

                partial_metadata[field_name] = value

            self._metadata = partial_metadata  # type: ignore

        return self._metadata  # type: ignore

    def convert_to_serialized_module_output(self) -> bytes:
        files_dict: Dict[str, bytes] = {}

        metadata = self._get_metadata()
        files_info_start = self._metadata_length + metadata['stdout_length'] + metadata['stderr_length']

        # Get all file info data at once
        files_info_buffer = InMemoryIndexableBuffer(data=self._buffer.get_data(
            start=files_info_start,
            length=metadata['files_info_length'],
        ))

        # Get all file data at once
        files_data_buffer = InMemoryIndexableBuffer(data=self._buffer.get_data(
            start=files_info_start + metadata['files_info_length'],
            length=metadata['files_data_length'],
        ))

        files_data_pointer = 0
        while files_info_buffer.pointer < len(files_info_buffer):
            path_length = files_info_buffer.get_data_with_pointer_as_int(self._file_path_length_bytes)
            path = files_info_buffer.get_data_with_pointer_as_string(path_length)
            data_length = files_info_buffer.get_data_with_pointer_as_int(self._file_data_length_bytes)

            data_start = files_data_pointer
            files_data_pointer += data_length

            files_dict[path] = files_data_buffer.get_data(start=data_start, length=data_length)

        return ModuleOutput().serialize(
            exit_code=self.get_exit_code(),
            files=files_dict,
            stderr=self.get_stderr(),
            stdout=self.get_stdout(),
        )

    @staticmethod
    def create_from_serialized_module_output(module_output_serialized: bytes) -> bytes:
        module_output_dict = ModuleOutput(module_output_serialized).deserialize()

        bbf_data = bytearray()
        bbf_data.extend(UnencryptedModuleOutput._version.to_bytes(1, 'big'))
        bbf_data.extend(UnencryptedModuleOutput._type.to_bytes(1, 'big'))

        # Length of stdout and stderr
        bbf_data.extend(len(module_output_dict['stdout']).to_bytes(8, 'big'))
        bbf_data.extend(len(module_output_dict['stderr']).to_bytes(8, 'big'))

        files_info = bytearray()
        files_data = bytearray()
        for path, data in module_output_dict['files'].items():
            encoded_path = path.encode()
            files_info.extend(len(encoded_path).to_bytes(4, 'big'))
            files_info.extend(encoded_path)
            files_info.extend(len(data).to_bytes(8, 'big'))

            files_data.extend(data)

        bbf_data.extend(len(files_info).to_bytes(8, 'big'))
        bbf_data.extend(len(files_data).to_bytes(8, 'big'))

        bbf_data.extend(module_output_dict['exit_code'].to_bytes(2, 'big'))
        bbf_data.extend(module_output_dict['stdout'])
        bbf_data.extend(module_output_dict['stderr'])
        bbf_data.extend(files_info)
        bbf_data.extend(files_data)

        return bbf_data
