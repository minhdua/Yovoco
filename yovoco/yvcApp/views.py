from yvcApp.models import Word, Collection, Vocabulary, VocabularyCollection, Typing
from yvcApp.serializers import WordSerializer, CollectionSerializer, VocabularySerializer, VocabularyCollectionSerializer, TypingSerializer
from rest_framework import viewsets

class WordViewSet(viewsets.ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer

class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

class VocabularyViewSet(viewsets.ModelViewSet):
    queryset = Vocabulary.objects.all()
    serializer_class = VocabularySerializer

class VocabularyCollectionViewSet(viewsets.ModelViewSet):
    queryset = VocabularyCollection.objects.all()
    serializer_class = VocabularyCollectionSerializer

class TypingViewSet(viewsets.ModelViewSet):
    queryset = Typing.objects.all()
    serializer_class = TypingSerializer


# Create your views here.
