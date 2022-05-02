from warnings import filters
from rest_framework.viewsets import ModelViewSet
from entities.models import Collection, Vocabulary
from entities.serializers import CollectionSerializer, VocabularySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from datetime import datetime
from copy import deepcopy

class CustomModelViewSet(ModelViewSet):
	filter_backends=(DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
	ordering_fields=('id',)
	
	def perform_create(self, serializer):
		user=self.request.user
		serializer.save(created_by=user, updated_by=user)
		
	def perform_update(self, serializer):
		serializer.update(self.get_object(), self.request.data)
		
	def perform_destroy(self, instance):
		instance.deleted_by=self.request.user
		instance.deleted_at=datetime.now()
		instance.save()
		
	def get_queryset(self):
		user=self.request.user
		return self.queryset.filter(created_by=user, deleted_by=None)
	
	def list(self, request, *args, **kwargs):
		response=super(CustomModelViewSet, self).list(request, *args, **kwargs)
		response.data.update({'detail': 'Success', 'status_code': status.HTTP_200_OK})
		print('response: ', response.data)
		return response

	def retrieve(self, request, *args, **kwargs):
		response=super(CustomModelViewSet, self).retrieve(request, *args, **kwargs)
		data=deepcopy(response.data)
		response.data={'detail': 'Success', 
						 'status_code': status.HTTP_200_OK,
						 'results': data}
		return response
	
	def create(self, request, *args, **kwargs):
		response=super(CustomModelViewSet, self).create(request, *args, **kwargs)
		data=deepcopy(response.data)
		response.data={'detail': 'Success', 
						 'status_code': status.HTTP_200_OK,
						 'results': data}
		return response
	
	def update(self, request, *args, **kwargs):
		response=super(CustomModelViewSet, self).update(request, *args, **kwargs)
		data=deepcopy(response.data)
		response.data={'detail': 'Success', 
						 'status_code': status.HTTP_200_OK,
						 'results': data}
		return response

class CollectionViewSet(CustomModelViewSet):
	queryset=Collection.objects.all()
	serializer_class=CollectionSerializer
	search_fields=('name','description')
	filterset_fields=('name',)
	
class VocabularyViewSet(CustomModelViewSet):
	queryset=Vocabulary.objects.all()
	serializer_class=VocabularySerializer
	search_fields=('^word', 'meaning', 'example', '=phonetic', '=pos', '=language', '^collection__name')
	filterset_fields=('word', 'pos', 'language', 'collection')