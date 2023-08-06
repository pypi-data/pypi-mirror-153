"""
Google cloud read-only storage.
"""
from logging import getLogger

from google.cloud import storage
from google.api_core.exceptions import NotFound

log = getLogger(__name__)


class GoogleCloudStorage:
    """
    Allows Site Configuration Client to read configurations from
    Google Cloud Storage bucket
    """
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.client = storage.Client()
        self.bucket = self.client.get_bucket(self.bucket_name)

    def read(self, file_path):
        """
        Gets the text content of a cloud storage bucket.
        If the file don't exists, it returns `None`.
        """
        blob = self.bucket.get_blob(file_path)
        try:
            return blob.download_as_bytes().decode('utf-8')
        except NotFound:
            log.warning('File path not found: %s', file_path)
            return None
