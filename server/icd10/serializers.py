from rest_framework import serializers
from .models import ResearchProject, ResearchItem, ICD10Item, ThematicCodeItem


class ResearchProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchProject
        fields = '__all__'


class ResearchItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchItem
        fields = '__all__'


class ICD10ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ICD10Item
        fields = '__all__'


class ThematicCodeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThematicCodeItem
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    icd10_item = ICD10ItemSerializer(many=False, read_only=True)

    class Meta:
        model = ResearchItem
        fields = '__all__'


class ResearchProjectNestedSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = ResearchProject
        fields = '__all__'
