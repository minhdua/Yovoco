from importlib.resources import path
from yvcApp.views import WordViewSet, CollectionViewSet, VocabularyViewSet, VocabularyCollectionViewSet, TypingViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# router.register(r'word', WordViewSet)
# router.register(r'collection', CollectionViewSet)
# router.register(r'vocabulary', VocabularyViewSet)
# router.register(r'vocabularycollection', VocabularyCollectionViewSet)
# router.register(r'typing', TypingViewSet)

urlpatterns = [
    # path('collection/', CollectionViewSet.as_view()),
]