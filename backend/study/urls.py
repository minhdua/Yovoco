from django.urls import path, include
from rest_framework.routers import DefaultRouter
from study.views import (LessonViewSet, 
						 LessonItemViewSet, 
						 LessonContentViewSet,
						 TestViewSet, 
						 QuizViewSet, 
						 QuizContentViewSet)
from yovoco.constants import *

router=DefaultRouter()
router.register(VALUE_LESSONS, LessonViewSet)
router.register(VALUE_LESSON_ITEMS, LessonItemViewSet)
router.register(VALUE_LESSON_CONTENTS, LessonContentViewSet)
router.register(VALUE_TESTS, TestViewSet)
router.register(VALUE_QUIZZES, QuizViewSet)
router.register(VALUE_QUIZ_CONTENTS, QuizContentViewSet)

urlpatterns=[
	path(VALUE_EMPTY_STRING, include(router.urls)),
]