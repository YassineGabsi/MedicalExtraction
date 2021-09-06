from abc import ABC, abstractmethod

from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

from icd10.core.validation import validate
from .core.exceptions import AlreadyExistsError, ValidationError
from .core.io import upload, upload_df
from .core.logging import logger
from .core.project import start_project, get_project_validated_data, process_project_validated_data
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
    ThematicCodeItemSerializer,
    ResearchProjectNestedSerializer,
    LogInSerializer,
    UserSerializer,
    ProfileSerializer
)


class SignUpView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class LogInView(TokenObtainPairView):
    serializer_class = LogInSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return get_user_model().objects.filter(username=self.request.user.username)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset)
        return obj


class FileUploadView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @csrf_exempt
    def post(self, requests, **kwargs):
        file_obj = requests.FILES.get('file', '')
        user = requests.user
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

        research_project = start_project(file_url, user)

        return JsonResponse({
            'message': 'Started',
            'file_url': research_project.project_file_url,
            'project_id': research_project.id,
            'start_date': research_project.start_date
        })


class AuthenticatedView(ABC):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class ResearchProjectCreateListView(AuthenticatedView, generics.ListCreateAPIView):
    serializer_class = ResearchProjectSerializer
    queryset = ResearchProject.objects.all()


class ResearchProjectView(AuthenticatedView, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ResearchProjectSerializer
    queryset = ResearchProject.objects.all()


class ResearchProjectInfoView(AuthenticatedView, generics.RetrieveAPIView):
    serializer_class = ResearchProjectNestedSerializer
    queryset = ResearchProject.objects.all()


class ResearchItemCreateListView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ResearchItemSerializer
    queryset = ResearchItem.objects.all()


class ResearchItemView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ResearchItemSerializer
    queryset = ResearchItem.objects.all()


class ICD10ItemCreateListView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ICD10ItemSerializer
    queryset = ICD10Item.objects.all()


class ICD10ItemView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ICD10ItemSerializer
    queryset = ICD10Item.objects.all()


class PercentView(ABC, APIView):
    permission_classes = (permissions.IsAuthenticated,)
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

        total_count = self.research_item_queryset.filter(project=project_id).count()
        in_progress_count = self.get_in_progress_count(project_id)

        return JsonResponse({
            "total_count": total_count,
            f"{self.TARGET}_count": in_progress_count,
            "percentage": "{0:.0%}".format(in_progress_count / total_count)
        })


class PredictedPercentView(PercentView):
    TARGET = "predicted"

    def get_in_progress_count(self, pk):
        return self.research_item_queryset.filter(project=pk).exclude(icd10_item__pk=None).count()


class ValidatedPercentView(PercentView):
    TARGET = "validated"

    def get_in_progress_count(self, pk):
        return self.research_item_queryset.filter(project=pk).filter(icd10_item__validated=True).count()


class PredictionAcceptedPercentView(PercentView):
    TARGET = "prediction_accepted"

    def get_in_progress_count(self, pk):
        return self.research_item_queryset.filter(project=pk) \
            .filter(icd10_item__prediction_accepted=True).count()


class GenerateProjectFileView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    research_item_queryset = ResearchItem.objects

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        try:
            project_id = kwargs['pk']
        except KeyError:
            return JsonResponse({"error": "Please provide a project id"}, status=400)

        user = request.user
        project = ResearchProject.objects.filter(user=user)
        if not project:
            return JsonResponse({"error": "Please provide a correct project id", "detail": "Not found."}, status=404)

        try:
            df = get_project_validated_data(project_id)
        except Exception as e:
            logger.exception(e)
            return JsonResponse({"error": "Failed to load project data"}, status=400)

        try:
            df = process_project_validated_data(df)
        except Exception as e:
            logger.exception(e)
            return JsonResponse({"error": "Could not prepare project data, please check your validation"}, status=400)

        try:
            file_url = upload_df(df, f"output/project_{project_id}.csv")
        except Exception as e:
            logger.exception(e)
            return JsonResponse({"error": "Could not upload result file"}, status=400)
        return JsonResponse({"file_url": file_url})
