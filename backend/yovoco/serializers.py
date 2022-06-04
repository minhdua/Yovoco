from rest_framework import serializers
from yovoco.models import Language

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
    model=Language