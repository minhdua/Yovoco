from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from datetime import datetime
from rest_framework import status
from yovoco.constants import *
from copy import deepcopy
from rest_framework.decorators import api_view, permission_classes
from yovoco.models import Language, PartOfSpeech, QuizType
from rest_framework.response import Response
class CustomModelViewSet(ModelViewSet):
	filter_backends=(DjangoFilterBackend, SearchFilter, OrderingFilter)
	ordering_fields=(KEY_ID,)
	
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
		response.data.update({KEY_DETAIL: MESSAGE_SUCCESS})
		return response

	def retrieve(self, request, *args, **kwargs):
		response=super(CustomModelViewSet, self).retrieve(request, *args, **kwargs)
		data=deepcopy(response.data)
		response.data={KEY_DETAIL: MESSAGE_SUCCESS, KEY_RESULTS: data}
		return response
	
	def create(self, request, *args, **kwargs):
		response=super(CustomModelViewSet, self).create(request, *args, **kwargs)
		data=deepcopy(response.data)
		response.data={KEY_DETAIL: MESSAGE_SUCCESS, KEY_RESULTS: data}
		return response
	
	def update(self, request, *args, **kwargs):
		response=super(CustomModelViewSet, self).update(request, *args, **kwargs)
		data=deepcopy(response.data)
		response.data={KEY_DETAIL: MESSAGE_SUCCESS, KEY_RESULTS: data}
		return response

def get_common_dto(members):
	results = []
	for member in members:
		data = {
			"name": member.name,
			"value": member.value,
			"label": member.label
		}
		results.append(data)
	return results

@api_view(['GET'])
def language_list(request):
	languages= Language.members()
	return Response({KEY_DETAIL: MESSAGE_SUCCESS, KEY_RESULTS: get_common_dto(languages)})

@api_view(['GET'])
def part_of_speech_list(request):
	poses = PartOfSpeech.members()
	return Response({KEY_DETAIL: MESSAGE_SUCCESS, KEY_RESULTS: get_common_dto(poses)})

@api_view(['GET'])
def quiz_type_list(request):
	quiz_types= QuizType.members()
	return Response({KEY_DETAIL: MESSAGE_SUCCESS, KEY_RESULTS: get_common_dto(quiz_types)})