from django.urls import path, include
from rest_framework.routers import DefaultRouter
from study.views import (LessonViewSet, 
						 LessonItemViewSet, 
						 LessonContentViewSet,
						 TestViewSet, 
						 QuizViewSet, 
						 QuizContentViewSet)

router=DefaultRouter()
router.register(r'lessons', LessonViewSet)
router.register(r'lesson-items', LessonItemViewSet)
router.register(r'lesson-contents', LessonContentViewSet)
router.register(r'tests', TestViewSet)
router.register(r'quizzes', QuizViewSet)
router.register(r'quiz-contents', QuizContentViewSet)

urlpatterns=[
	path('', include(router.urls)),
]