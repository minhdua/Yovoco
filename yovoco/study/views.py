from study.serializers import (LessonSerializer, 
                               LessonItemSerializer,
                               TestSerializer,
                                QuizSerializer,
                                QuizContentSerializer,
                                LessonContentSerializer)
from study.models import (Lesson, LessonItem, LessonContent, Test, Quiz, QuizContent)
from entities.views import CustomModelViewSet
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

class LessonViewSet(CustomModelViewSet):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    
class LessonItemViewSet(CustomModelViewSet):
    serializer_class = LessonItemSerializer
    queryset = LessonItem.objects.all()
    
class LessonContentViewSet(CustomModelViewSet):
    serializer_class = LessonContentSerializer
    queryset = LessonContent.objects.all()

class TestViewSet(CustomModelViewSet):
    serializer_class = TestSerializer
    queryset = Test.objects.all()

class QuizViewSet(CustomModelViewSet):
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()

class QuizContentViewSet(CustomModelViewSet):
    serializer_class = QuizContentSerializer
    queryset = QuizContent.objects.all()

