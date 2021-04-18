import os

from django.core.files.uploadedfile import TemporaryUploadedFile

from icd10.core.exceptions import AlreadyExistsError
from icd10.storages import MediaStorage


def upload(file_obj: TemporaryUploadedFile):
    file_directory_within_bucket = 'uploads/'

    file_path_within_bucket = os.path.join(
        file_directory_within_bucket,
        file_obj.name
    )

    media_storage = MediaStorage()

    if not media_storage.exists(file_path_within_bucket):
        media_storage.save(file_path_within_bucket, file_obj)
        file_url = media_storage.url(file_path_within_bucket)
    else:
        raise AlreadyExistsError(
            "Error: file {filename} already exists at {file_directory} in bucket {bucket_name}".format(
                filename=file_obj.name,
                file_directory=file_directory_within_bucket,
                bucket_name=media_storage.bucket_name
            )
        )
    return file_url
