from concurrent.futures.thread import ThreadPoolExecutor
import os

thread_pool = ThreadPoolExecutor(max_workers=2)
BUCKET = os.getenv("AWS_STORAGE_BUCKET_NAME", "icd10-entity-recognition")