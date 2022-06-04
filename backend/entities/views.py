from entities.models import Collection, Vocabulary
from entities.serializers import CollectionSerializer, VocabularySerializer
from yovoco.constants import *
from yovoco.views import CustomModelViewSet
class CollectionViewSet(CustomModelViewSet):
	queryset=Collection.objects.all()
	serializer_class=CollectionSerializer
	search_fields=(KEY_NAME,KEY_DESCRIPTION)
	filterset_fields=(KEY_NAME,)
	
class VocabularyViewSet(CustomModelViewSet):
	queryset=Vocabulary.objects.all()
	serializer_class=VocabularySerializer
	search_fields=(SEARCH_WORD, SEARCH_MEANING, SEARCH_EXAMPLE, SEARCH_PHONETIC, SEARCH_POS,\
			SEARCH_LANGUAGE, SEARCH_COLLECTION_NAME)
	filterset_fields=(KEY_WORD, KEY_POS, KEY_LANGUAGE, KEY_COLLECTION)