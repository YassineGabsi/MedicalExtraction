from django.shortcuts import render

import os

from django.views import View
from rest_framework.views import APIView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from icd10.storages import MediaStorage
from icd10.core.validation import validate

class FileUploadView(APIView):
    @csrf_exempt
    def post(self, requests, **kwargs):
        file_obj = requests.FILES.get('file', '')
        validation = validate(file_obj)
        if not validation["valid"]:
            return JsonResponse({
                'message': validation["error"]
            }, status=400)

        file_directory_within_bucket = 'uploads/'

        file_path_within_bucket = os.path.join(
            file_directory_within_bucket,
            file_obj.name
        )

        media_storage = MediaStorage()

        if not media_storage.exists(file_path_within_bucket): 
            media_storage.save(file_path_within_bucket, file_obj)
            file_url = media_storage.url(file_path_within_bucket)

            return JsonResponse({
                'message': 'OK',
                'fileUrl': file_url,
            })
        else:
            return JsonResponse({
                'message': 'Error: file {filename} already exists at {file_directory} in bucket {bucket_name}'.format(
                    filename=file_obj.name,
                    file_directory=file_directory_within_bucket,
                    bucket_name=media_storage.bucket_name
                ),
            }, status=400)