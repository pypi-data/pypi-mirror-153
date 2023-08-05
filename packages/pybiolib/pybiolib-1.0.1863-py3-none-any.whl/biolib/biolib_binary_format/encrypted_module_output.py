import base64

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from biolib.biolib_binary_format import BioLibBinaryFormatBasePackage
from biolib.biolib_binary_format.utils import IndexableBuffer, InMemoryIndexableBuffer
from biolib.biolib_binary_format.common_types import FilesInfo
from biolib.biolib_binary_format.module_output import ModuleOutput
from biolib.typing_utils import Optional, TypedDict, List

IV_LENGTH_BYTES = 12
TAG_LENGTH_BYTES = 16


class EncryptedModuleOutputMetadata(TypedDict):
    version: int
    type: int
    stdout_length: int
    stderr_length: int
    files_info_length: int
    files_data_length: int


encrypted_module_output_metadata_lengths = dict(
    # Note: order is important
    version=1,
    type=1,
    stdout_length=8,
    stderr_length=8,
    files_info_length=8,
    files_data_length=8,
)


class EncryptedModuleOutputError(BaseException):
    pass


class EncryptedModuleOutputWithKey(BioLibBinaryFormatBasePackage):
    _TYPE = 12
    _VERSION = 1

    def __init__(self, aes_key_string_b64: str, buffer: Optional[IndexableBuffer] = None):
        super().__init__()
        self._aes_key_buffer: bytes = base64.urlsafe_b64decode(aes_key_string_b64.encode())
        self._buffer: Optional[IndexableBuffer] = buffer

    def _get_metadata(self) -> EncryptedModuleOutputMetadata:
        if not self._buffer:
            raise EncryptedModuleOutputError(
                'You must construct this class with a buffer to get its metadata'
            )

        metadata = {}
        for field_name, field_length in encrypted_module_output_metadata_lengths.items():
            value = self._buffer.get_data_with_pointer_as_int(length=field_length)
            if field_name == 'version' and value != EncryptedModuleOutputWithKey._VERSION:
                raise Exception('Version does not match')

            if field_name == 'type' and value != EncryptedModuleOutputWithKey._TYPE:
                raise Exception('Type does not match')

            metadata[field_name] = value

        return EncryptedModuleOutputMetadata(**metadata)  # type: ignore

    @property
    def _metadata_length_bytes(self) -> int:
        return sum(encrypted_module_output_metadata_lengths.values())

    def convert_to_serialized_module_output(self) -> bytes:
        if not self._buffer:
            raise EncryptedModuleOutputError('You must construct this class with a buffer to convert to module output')

        metadata = self._get_metadata()
        exit_code_bytes = self._decrypt(
            self._buffer.get_data_with_pointer(length=2 + IV_LENGTH_BYTES + TAG_LENGTH_BYTES)
        )
        exit_code = int.from_bytes(exit_code_bytes, 'big')

        stdout = self._decrypt(
            self._buffer.get_data_with_pointer(length=metadata['stdout_length'])
        )

        stderr = self._decrypt(
            self._buffer.get_data_with_pointer(length=metadata['stderr_length'])
        )

        files_info_serialized = InMemoryIndexableBuffer(self._decrypt(
            self._buffer.get_data_with_pointer(length=metadata['files_info_length'])
        ))

        files_info: List[FilesInfo] = []
        while files_info_serialized.pointer <= len(files_info_serialized) - 1:  # subtract 1 as pointer is 0-indexed
            path_length = files_info_serialized.get_data_with_pointer_as_int(length=4)
            files_info.append({
                'path': files_info_serialized.get_data_with_pointer(length=path_length).decode(),
                'data_length': files_info_serialized.get_data_with_pointer_as_int(length=8)
            })

        files = {}
        for file_info in files_info:
            files[file_info['path']] = self._decrypt(
                self._buffer.get_data_with_pointer(length=file_info['data_length'])
            )

        return ModuleOutput().serialize(
            stdout=stdout,
            stderr=stderr,
            exit_code=exit_code,
            files=files
        )

    def create_from_serialized_module_output(self, module_output_serialized: bytes) -> bytes:
        module_output_dict = ModuleOutput(module_output_serialized).deserialize()

        bbf_data = bytearray()
        bbf_data.extend(EncryptedModuleOutputWithKey._VERSION.to_bytes(1, 'big'))
        bbf_data.extend(EncryptedModuleOutputWithKey._TYPE.to_bytes(1, 'big'))

        encrypted_stdout = self._encrypt(module_output_dict['stdout'])
        encrypted_stderr = self._encrypt(module_output_dict['stderr'])

        files_info = bytearray()
        encrypted_files_data = bytearray()
        for path, data in module_output_dict['files'].items():
            encoded_path = path.encode()
            files_info.extend(len(encoded_path).to_bytes(4, 'big'))
            files_info.extend(encoded_path)

            encrypted_data = self._encrypt(data)
            files_info.extend(len(encrypted_data).to_bytes(8, 'big'))
            encrypted_files_data.extend(encrypted_data)

        encrypted_files_info = self._encrypt(files_info)

        # Length of encrypted stdout and stderr
        bbf_data.extend(len(encrypted_stdout).to_bytes(8, 'big'))
        bbf_data.extend(len(encrypted_stderr).to_bytes(8, 'big'))

        bbf_data.extend(len(encrypted_files_info).to_bytes(8, 'big'))
        bbf_data.extend(len(encrypted_files_data).to_bytes(8, 'big'))

        bbf_data.extend(self._encrypt(
            module_output_dict['exit_code'].to_bytes(2, 'big')
        ))
        bbf_data.extend(encrypted_stdout)
        bbf_data.extend(encrypted_stderr)

        bbf_data.extend(encrypted_files_info)
        bbf_data.extend(encrypted_files_data)

        return bbf_data

    def _encrypt(self, data: bytes) -> bytes:
        iv = get_random_bytes(12)
        aes_key = AES.new(self._aes_key_buffer, AES.MODE_GCM, iv)
        encrypted_data, tag = aes_key.encrypt_and_digest(data)  # type: ignore
        return iv + encrypted_data + tag

    def _decrypt(self, data: bytes) -> bytes:
        iv = data[0:IV_LENGTH_BYTES]
        tag = data[-TAG_LENGTH_BYTES:]
        data = data[IV_LENGTH_BYTES:-TAG_LENGTH_BYTES]
        cipher = AES.new(self._aes_key_buffer, AES.MODE_GCM, iv)
        plaintext = cipher.decrypt(data)
        try:
            cipher.verify(tag)  # type: ignore
            return plaintext
        except ValueError as error:
            raise EncryptedModuleOutputError('Decryption failed: Key incorrect or message corrupted') from error
