from django.db import models
import uuid

class ResearchProject(models.Model):
    STATUSES = (
        ('S', 'Started'),
        ('C', 'Completed'),
        ('E', 'Error'),
    )
    start_date = models.DateTimeField(default=None)
    end_date = models.DateTimeField(default=None)
    status = models.CharField(max_length=30, choices=STATUSES)
    project_file_url = models.CharField(max_length=256, default=None, null=True)

class ResearchItem(models.Model):
    project_id = models.ForeignKey(ResearchProject, on_delete=models.CASCADE)
    title = models.TextField()
    synopsis = models.TextField()
    inclusion_criteria = models.TextField()


class ICD10Item(models.Model):
    item_id = models.OneToOneField(ResearchItem, on_delete=models.CASCADE)
    icd10_chapter_predicted = models.CharField(max_length=30)
    icd10_block_predicted = models.CharField(max_length=30)
    icd10_chapter = models.CharField(max_length=30)
    icd10_block = models.CharField(max_length=30)
    medical_terms = models.JSONField(default=None, blank=True, null=True)
    prediction_accepted = models.BooleanField(blank=True, null=True)
    validated = models.BooleanField(default=False)


class ThematicCodeItem(models.Model):
    THEMATIC_CODES = (
        ('S', 'Social Care'),
        ('O', 'Obesity'),
        ('Di', 'Diabetes'),
        ('De', 'Dementia'),
        ('A', 'Antimicrobrial Resistance'),
    )
    item_id = models.OneToOneField(ResearchItem, on_delete=models.CASCADE)
    thematic_code = models.CharField(max_length=30, choices=THEMATIC_CODES)
