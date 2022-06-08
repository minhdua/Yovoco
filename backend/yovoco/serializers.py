from rest_framework.serializers import ModelSerializer
from yovoco.models import Language

class LanguageSerializer(ModelSerializer):
    class Meta:
        model=Language
        