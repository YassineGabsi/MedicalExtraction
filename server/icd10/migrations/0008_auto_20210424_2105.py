# Generated by Django 3.1.3 on 2021-04-24 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icd10', '0007_auto_20210424_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='icd10item',
            name='icd10_validation',
            field=models.JSONField(blank=True, default=None, null=True),
        ),
    ]