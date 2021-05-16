from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

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

class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Passwords must match.')
        return data

    def create(self, validated_data):
        data = {
            key: value for key, value in validated_data.items()
            if key not in ('password1', 'password2')
        }
        data['password'] = validated_data['password1']
        return self.Meta.model.objects.create_user(**data)

    class Meta:
        model = get_user_model()
        fields = (
            'id', 'username', 'password1', 'password2',
            'first_name', 'last_name', 'email', 'image_url'
        )
        read_only_fields = ('id',)


class LogInSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = UserSerializer(user).data
        for key, value in user_data.items():
            if key != 'id':
                token[key] = value
        return token


class ProfileSerializer(serializers.ModelSerializer):
    projects = ResearchProjectSerializer(many=True, read_only=True)
    # projects = serializers.PrimaryKeyRelatedField(many=True, queryset=ResearchProject.objects.all())
    class Meta:
        model = get_user_model()
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'credits', 'image_url', 'projects'
        )
        read_only_fields = ('id', 'created', 'updated',)
