from storages.backends.s3boto3 import S3Boto3Storage

from icd10.core.common import BUCKET


class MediaStorage(S3Boto3Storage):
    bucket_name = BUCKET