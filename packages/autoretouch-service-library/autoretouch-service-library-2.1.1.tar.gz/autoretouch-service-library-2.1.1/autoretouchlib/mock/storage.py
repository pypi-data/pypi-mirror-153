from typing import Union
from fastapi import HTTPException

from autoretouchlib.types import FileContentHash, OrganizationId, FileType


class MockStorage:
    def __init__(self):
        self.__storage = {}

    def load(self, content_hash: Union[FileContentHash, str], organization_id: OrganizationId) -> bytes:
        if isinstance(content_hash, str):
            content_hash = FileContentHash(content_hash)
        key = organization_id + "/origin/" + content_hash.get_value()
        try:
            return self.__storage[key]
        except KeyError:
            raise HTTPException(status_code=404)

    def store(self, blob: bytes, content_type: Union[FileType, str], organization_id: OrganizationId) \
            -> FileContentHash:
        if isinstance(content_type, str):
            content_type = FileType(content_type)
        content_hash = FileContentHash.from_bytes(blob)
        self.__storage[organization_id + "/origin/" + content_hash.get_value()] = blob
        return content_hash
