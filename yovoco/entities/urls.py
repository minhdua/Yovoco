from django.urls import path,include
from rest_framework.routers import DefaultRouter
from entities.views import CollectionViewSet, VocabularyViewSet

router = DefaultRouter()
router.register(r'collections', CollectionViewSet)
router.register(r'vocabularies', VocabularyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]