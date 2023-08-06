import hashlib
import re
from enum import Enum

OrganizationId = str


class FileType(Enum):
    PNG = 'image/png'
    JPEG = 'image/jpeg'
    TIFF = 'image/tiff'
    PSD = 'image/vnd.adobe.photoshop'
    JSON = 'application/json'
    XML = 'application/rdf+xml'
    ICC = 'application/vnd.iccprofile'
    HEIC = 'image/heic'


class FileContentHash:
    def __init__(self, value: str):
        if not re.fullmatch(r"^[A-Fa-f0-9]{64}$", value):
            raise RuntimeError(f"invalid content hash {value}")
        self.__value = value

    @staticmethod
    def from_bytes(byte_content: bytes):
        return FileContentHash(hashlib.sha256(byte_content).digest().hex().lower())

    def get_value(self) -> str:
        return self.__value

    def __repr__(self):
        return f"FileContentHash({self.__value})"

    def __str__(self):
        return self.__value
