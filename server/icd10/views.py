from abc import ABC, abstractmethod

from rest_framework import generics
from rest_framework.views import APIView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from icd10.core.validation import validate
from .core.exceptions import AlreadyExistsError, ValidationError
from .core.io import upload
from .core.project import start_project
from .models import (
    ResearchProject,
    ResearchItem,
    ICD10Item,
    ThematicCodeItem
)
from .serializers import (
    ResearchProjectSerializer,
    ResearchItemSerializer,
    ICD10ItemSerializer,
    ThematicCodeItemSerializer
)


class FileUploadView(APIView):
    @csrf_exempt
    def post(self, requests, **kwargs):
        file_obj = requests.FILES.get('file', '')
        try:
            validate(file_obj)
        except ValidationError as e:
            return JsonResponse({
                'message': str(e)
            }, status=400)

        try:
            file_url = upload(file_obj)
        except AlreadyExistsError as e:
            return JsonResponse({
                'message': str(e),
            }, status=400)

        print("**************", file_url, "**********************")
        research_project = start_project(file_url)

        return JsonResponse({
            'message': 'Started',
            'fileUrl': research_project.project_file_url,
            'project_id': research_project.id,
            'start_date': research_project.start_date
        })


class ResearchProjectCreateListView(generics.ListCreateAPIView):
    serializer_class = ResearchProjectSerializer
    queryset = ResearchProject.objects.all()


class ResearchProjectView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ResearchProjectSerializer
    queryset = ResearchProject.objects.all()


class ResearchItemCreateListView(generics.ListCreateAPIView):
    serializer_class = ResearchItemSerializer
    queryset = ResearchItem.objects.all()


class ResearchItemView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ResearchItemSerializer
    queryset = ResearchItem.objects.all()


class ICD10ItemCreateListView(generics.ListCreateAPIView):
    serializer_class = ICD10ItemSerializer
    queryset = ICD10Item.objects.all()


class ICD10ItemView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ICD10ItemSerializer
    queryset = ICD10Item.objects.all()


class PercentView(ABC, APIView):
    research_item_queryset = ResearchItem.objects
    TARGET: str

    @abstractmethod
    def get_in_progress_count(self, pk: int) -> int:
        raise NotImplemented("Please implement the get_in_progress_count method")

    def get(self, request, *args, **kwargs):
        try:
            project_id = kwargs['pk']
        except KeyError:
            return JsonResponse({"error": "Not found"}, status=400)

        total_count = self.research_item_queryset.filter(project_id=project_id).count()
        in_progress_count = self.get_in_progress_count(project_id)

        return JsonResponse({
            "total_count": total_count,
            f"{self.TARGET}_count": in_progress_count,
            "percentage": "{0:.0%}".format(in_progress_count / total_count)
        })


class PredictedPercentView(PercentView):
    TARGET = "predicted"

    def get_in_progress_count(self, pk):
        return self.research_item_queryset.filter(project_id=pk).exclude(icd10item__pk=None).count()


class ValidatedPercentView(PercentView):
    TARGET = "validated"

    def get_in_progress_count(self, pk):
        return self.research_item_queryset.filter(project_id=pk).filter(icd10item__validated=True).count()


class PredictionAcceptedPercentView(PercentView):
    TARGET = "prediction_accepted"

    def get_in_progress_count(self, pk):
        return self.research_item_queryset.filter(project_id=pk) \
            .filter(icd10item__prediction_accepted=True).count()
