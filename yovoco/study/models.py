from calendar import c
from math import fabs
from django.db import models
from entities.models import Vocabulary
from yovoco.models import AuditModel, QuizType
from yovoco.utils import now_to_string
from yovoco.constants import *
import uuid
class Lesson(AuditModel):
	"""
	Lesson
	"""
	name=models.CharField(max_length=50, default=now_to_string())
	description=models.CharField(max_length=200, default=VALUE_DESCRIPTION_DEFAULT,blank=True, null=True)
 
	class Meta:
		db_table=VALUE_LESSON_TABLE
class LessonItem(AuditModel):
	"""
	LessonItem
	"""
	vocabulary=models.ForeignKey(Vocabulary, on_delete=models.CASCADE)
	typing_count=models.IntegerField(default=0)
	right_count=models.IntegerField(default=0)
	wrong_list=models.CharField(max_length=200, blank=True, null=True)

	class Meta:
		db_table=VALUE_LESSON_ITEM_TABLE
  
class LessonContent(AuditModel):
	"""
	LessonContent
	"""
	lesson=models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name=VALUE_LESSON_CONTENT)
	item=models.ForeignKey(LessonItem, on_delete=models.CASCADE, related_name=VALUE_ITEM_CONTENT)
	
	class Meta:
		db_table=VALUE_LESSON_CONTENT_TABLE
class Test(AuditModel):
	"""
	Test
	"""
	name=models.CharField(max_length=50, default=now_to_string())
	description=models.CharField(max_length=200, default=VALUE_DESCRIPTION_DEFAULT,blank=True, null=True)
	
	class Meta:
		db_table=VALUE_TEST_TABLE
class Quiz(AuditModel):
	"""
	Quiz
	"""
	question=models.CharField(max_length=200, blank=True, null=True)
	answer1=models.CharField(max_length=50, default=VALUE_ANSWER_DEFAULT, blank=True, null=True)
	answer2=models.CharField(max_length=50, default=VALUE_ANSWER_DEFAULT, blank=True, null=True)
	answer3=models.CharField(max_length=50, default=VALUE_ANSWER_DEFAULT, blank=True, null=True)
	vocabulary=models.ForeignKey(Vocabulary, on_delete=models.CASCADE)
	correct_answer=models.CharField(max_length=50, blank=True, null=True)
	question_type=models.CharField(max_length=50, choices=QuizType.choices, default=QuizType.FIND_MEANING)
	
	class Meta:
		db_table=VALUE_QUIZ_TABLE
class QuizContent(AuditModel):
	"""
	QuizContent
	"""
	test=models.ForeignKey(Test, on_delete=models.CASCADE, related_name=VALUE_TEST_CONTENT)
	quiz=models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name=VALUE_TEST_CONTENT)
	client_answer=models.CharField(max_length=50, blank=True, null=True)
	test_times=models.IntegerField(default=0)
	
	class Meta:
		db_table=VALUE_QUIZ_CONTENT_TABLE