"""medical_extraction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

from icd10.views import FileUploadView
from icd10.views import (
    ResearchProjectCreateListView,
    ResearchProjectView,
    ResearchItemCreateListView,
    ResearchItemView,
    ICD10ItemCreateListView,
    ICD10ItemView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
    path('openapi', get_schema_view(
        title="Medical Extraction API",
        description="REST API",
        public=True
    ), name='openapi-schema'),
    path('api/upload/', FileUploadView.as_view()),
    path('api/project/<int:pk>', ResearchProjectView.as_view(), name='project'),
    path('api/project',ResearchProjectCreateListView.as_view(), name='project-create-list'),
    path('api/item/<int:pk>', ResearchItemView.as_view(), name='item'),
    path('api/item',ResearchItemCreateListView.as_view(), name='item-create-list'),


]