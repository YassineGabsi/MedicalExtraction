from django.db import models
from django.contrib.auth.models import AbstractUser


class ResearchProject(models.Model):
    STATUSES = (
        ('S', 'Started'),
        ('C', 'Completed'),
        ('E', 'Error'),
    )
    start_date = models.DateTimeField(auto_now_add=True, blank=True)
    end_date = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUSES, default='S')
    project_file_url = models.TextField(default=None, null=True)


class ResearchItem(models.Model):
    project = models.ForeignKey(ResearchProject, related_name='items', on_delete=models.CASCADE)
    title = models.TextField()
    research_summary = models.TextField()
    inclusion_criteria = models.TextField()


class ICD10Item(models.Model):
    item = models.OneToOneField(ResearchItem, related_name='icd10_item', on_delete=models.CASCADE)
    icd10_prediction = models.JSONField()
    icd10_validation = models.JSONField(default=None, blank=True, null=True)
    medical_terms = models.JSONField(default=None, blank=True, null=True)
    first_prediction_accepted = models.BooleanField(blank=True, null=True)
    validated = models.BooleanField(default=False)


class ThematicCodeItem(models.Model):
    THEMATIC_CODES = (
        ('S', 'Social Care'),
        ('O', 'Obesity'),
        ('Di', 'Diabetes'),
        ('De', 'Dementia'),
        ('A', 'Antimicrobrial Resistance'),
    )
    item = models.OneToOneField(ResearchItem, on_delete=models.CASCADE)
    thematic_code = models.CharField(max_length=30, choices=THEMATIC_CODES)


class User(AbstractUser):
    credits = models.IntegerField(default=1000)
    image_url = models.CharField(max_length=255, null=True)
