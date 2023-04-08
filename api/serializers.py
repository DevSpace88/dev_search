from rest_framework import serializers
from projects.models import Project

# modelserializer konvertiert das Project model in ein json-objekt
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'