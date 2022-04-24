from rest_framework.serializers import ModelSerializer
from yvcApp.models import Word, Collection, Vocabulary, VocabularyCollection, Typing

read_only_fields = ('created_at', 'updated_at', 'created_by', 'updated_by', 'is_deleted', 'deleted_by', 'deleted_at')

class WordSerializer(ModelSerializer):
    class Meta:
        model = Word
        fields = '__all__'
        read_only_fields = read_only_fields

class CollectionSerializer(ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'
        read_only_fields = read_only_fields

class VocabularySerializer(ModelSerializer):
    class Meta:
        model = Vocabulary
        fields = '__all__'
        read_only_fields = read_only_fields

class VocabularyCollectionSerializer(ModelSerializer):
    class Meta:
        model = VocabularyCollection
        fields = '__all__'
        read_only_fields = read_only_fields

class TypingSerializer(ModelSerializer):
    class Meta:
        model = Typing
        fields = '__all__'
        read_only_fields = read_only_fields
