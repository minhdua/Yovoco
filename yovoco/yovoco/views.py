from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from datetime import datetime
from rest_framework import status
from yovoco.constants import *
from copy import deepcopy

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
		response.data.update({KEY_DETAIL: MESSAGE_SUCCESS, KEY_STATUS_CODE: status.HTTP_200_OK})
		return response

	def retrieve(self, request, *args, **kwargs):
		response=super(CustomModelViewSet, self).retrieve(request, *args, **kwargs)
		data=deepcopy(response.data)
		response.data={KEY_DETAIL: MESSAGE_SUCCESS, KEY_STATUS_CODE: status.HTTP_200_OK, KEY_RESULTS: data}
		return response
	
	def create(self, request, *args, **kwargs):
		response=super(CustomModelViewSet, self).create(request, *args, **kwargs)
		data=deepcopy(response.data)
		response.data={KEY_DETAIL: MESSAGE_SUCCESS, KEY_STATUS_CODE: status.HTTP_200_OK, KEY_RESULTS: data}
		return response
	
	def update(self, request, *args, **kwargs):
		response=super(CustomModelViewSet, self).update(request, *args, **kwargs)
		data=deepcopy(response.data)
		response.data={KEY_DETAIL: MESSAGE_SUCCESS, KEY_STATUS_CODE: status.HTTP_200_OK, KEY_RESULTS: data}
		return response