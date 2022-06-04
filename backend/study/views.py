import re
from study.serializers import (LessonSerializer, 
								LessonItemSerializer,
								TestSerializer,
								QuizSerializer,
								QuizContentSerializer,
								LessonContentSerializer)
from study.models import (Lesson, LessonItem, LessonContent, Test, Quiz, QuizContent)
from entities.views import CustomModelViewSet
from yovoco.constants import *
from study.serializers import get_quiz_dto
class LessonViewSet(CustomModelViewSet):
	serializer_class=LessonSerializer
	queryset=Lesson.objects.all()
	
class LessonItemViewSet(CustomModelViewSet):
	serializer_class=LessonItemSerializer
	queryset=LessonItem.objects.all()
	
class LessonContentViewSet(CustomModelViewSet):
	serializer_class=LessonContentSerializer
	queryset=LessonContent.objects.all()

class TestViewSet(CustomModelViewSet):
	serializer_class=TestSerializer
	queryset=Test.objects.all()

class QuizViewSet(CustomModelViewSet):
	serializer_class=QuizSerializer
	queryset=Quiz.objects.all()
 
	def retrieve(self, request, *args, **kwargs):
		response=super(CustomModelViewSet, self).retrieve(request, *args, **kwargs)
		response.data=get_quiz_dto(response.data)
		response.data={KEY_DETAIL: MESSAGE_SUCCESS, KEY_RESULTS: response.data}
		return response

	def list(self, request, *args, **kwargs):
		response=super(CustomModelViewSet, self).list(request, *args, **kwargs)
		results=[]
		for result in response.data[KEY_RESULTS]:
			data=get_quiz_dto(result)
			results.append(data)
		response.data={KEY_DETAIL: MESSAGE_SUCCESS, KEY_RESULTS: results}
		return response

class QuizContentViewSet(CustomModelViewSet): 
	serializer_class=QuizContentSerializer
	queryset=QuizContent.objects.all()