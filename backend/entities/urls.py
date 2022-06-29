from django.urls import path,include
from rest_framework.routers import DefaultRouter
from entities.views import CollectionViewSet
from yovoco.constants import *
from entities import views

router=DefaultRouter()
router.register(VALUE_COLLECTIONS, CollectionViewSet)
# router.register(VALUE_VOCABULARIES, VocabularyViewSet)

urlpatterns=[
	path(VALUE_EMPTY_STRING, include(router.urls)),
	path('vocabularies/', views.search_vocabulary)
]