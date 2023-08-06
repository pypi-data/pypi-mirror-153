import logging
import os
from typing import Union

from fastapi import HTTPException
from google.cloud.exceptions import NotFound, GoogleCloudError
from google.cloud import storage as google_cloud_storage

from autoretouchlib.types import FileContentHash, OrganizationId, FileType


class Storage:
    def __init__(self):
        bucket_name = os.getenv("IMAGES_BUCKET")
        project = os.getenv("GOOGLE_PROJECT")
        self.storage_client = google_cloud_storage.Client(project=project)
        self.bucket = self.storage_client.bucket(bucket_name, project)

    def load(self, content_hash: Union[FileContentHash, str], organization_id: OrganizationId
             ) -> bytes:
        if isinstance(content_hash, str):
            content_hash = FileContentHash(content_hash)
        try:
            blob = self.bucket.blob(f"{organization_id}/origin/{content_hash.get_value()}")
            return blob.download_as_bytes()
        except NotFound:
            raise HTTPException(status_code=404)

    def store(self, blob: bytes, content_type: Union[FileType, str], organization_id: OrganizationId
              ) -> FileContentHash:
        if isinstance(content_type, str):
            content_type = FileType(content_type)
        content_hash = FileContentHash.from_bytes(blob)
        bucket_blob = self.bucket.blob(f"{organization_id}/origin/{content_hash.get_value()}")
        if not bucket_blob.exists():
            try:
                bucket_blob.upload_from_string(data=blob, content_type=content_type.value)
            except GoogleCloudError as e:
                logging.error(
                    f"GoogleCloudError in storing {content_hash.get_value()} for organization {organization_id}: " + e)
                # bucket_blob.delete()
                raise e
        return content_hash


storage = Storage()
