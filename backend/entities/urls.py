from django.urls import path,include
from rest_framework.routers import DefaultRouter
from entities.views import CollectionViewSet, VocabularyViewSet
from yovoco.constants import *

router=DefaultRouter()
router.register(VALUE_COLLECTIONS, CollectionViewSet)
router.register(VALUE_VOCABULARIES, VocabularyViewSet)

urlpatterns=[
	path(VALUE_EMPTY_STRING, include(router.urls)),
]