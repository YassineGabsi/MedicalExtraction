import io
import os
from datetime import datetime

import boto3
import pandas as pd
from django.core.files.uploadedfile import TemporaryUploadedFile

from icd10.core.common import BUCKET
from icd10.core.exceptions import AlreadyExistsError
from icd10.core.loaders import generic_read
from icd10.core.utils import append_id
from icd10.storages import MediaStorage
from medical_extraction.settings import ALLOW_DUPLICATE_FILES

s3_client = boto3.client('s3')


def upload(file_obj: TemporaryUploadedFile):
    file_directory_within_bucket = 'uploads/'

    file_path_within_bucket = os.path.join(
        file_directory_within_bucket,
        file_obj.name if not ALLOW_DUPLICATE_FILES else
        append_id(file_obj.name, int(datetime.timestamp(datetime.now())))
    )

    media_storage = MediaStorage()

    if not media_storage.exists(file_path_within_bucket):
        media_storage.save(file_path_within_bucket, file_obj)
        file_url = f"https://{media_storage.bucket_name}.s3.amazonaws.com/{file_path_within_bucket}"
        #file_url = media_storage.url(file_path_within_bucket)
    else:
        raise AlreadyExistsError(
            "Error: file {filename} already exists at {file_directory} in bucket {bucket_name}".format(
                filename=file_obj.name,
                file_directory=file_directory_within_bucket,
                bucket_name=media_storage.bucket_name
            )
        )
    return file_url


def read(file_url: str) -> pd.DataFrame:
    return generic_read(file_url)


def upload_df(df: pd.DataFrame, key: str):
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    media_storage = MediaStorage()
    media_storage.save(key, buffer)
    return f"https://{media_storage.bucket_name}.s3.amazonaws.com/{key}"
