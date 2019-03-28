from rest_framework import serializers

from models import *


class JobSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    project_hpc = serializers.CharField(source='project.hpc', read_only=True)

    class Meta:
        model = Job
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class QuotaSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    project_hpc = serializers.CharField(source='project.hpc', read_only=True)

    class Meta:
        model = Quota
        fields = '__all__'
