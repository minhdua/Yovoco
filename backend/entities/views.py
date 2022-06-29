from entities.models import Collection, Vocabulary
from entities.serializers import CollectionSerializer, VocabularySerializer
from yovoco.constants import *
from yovoco.views import CustomModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
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
 
@api_view(['GET'])
@permission_classes([AllowAny])
def search_vocabulary(request):
	serializers = VocabularySerializer()
	data = serializers.list(request)
	return Response(data,status=status.HTTP_200_OK)