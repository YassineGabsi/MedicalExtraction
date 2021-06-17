from rest_framework.views import APIView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


class HealthCheckView(APIView):
    @csrf_exempt
    def get(self, requests, **kwargs):
        return JsonResponse({
            'message': 'Ok',
        })