from django.db import models
from entities.models import (AuditModel, 
							 Vocabulary,
							 now_to_string)

class Lesson(AuditModel):
	"""
	Lesson
	"""
	name=models.CharField(max_length=50, default=now_to_string)
	description=models.CharField(max_length=200, blank=True, null=True)
 
class LessonItem(AuditModel):
	"""
	LessonItem
	"""
	vocabulary=models.ForeignKey(Vocabulary, on_delete=models.CASCADE)
	typing_count=models.IntegerField(default=0)
	right_count=models.IntegerField(default=0)
	wrong_list=models.CharField(max_length=200, blank=True, null=True)

class LessonContent(AuditModel):
	"""
	LessonContent
	"""
	lesson=models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_content')
	item=models.ForeignKey(LessonItem, on_delete=models.CASCADE, related_name='item_content')
	
class QuizType(models.TextChoices):
	"""
	QuizType
	"""
	FIND_MEANING='fm', 'Find Meaning'
	FIND_WORD='fw', 'Find Word'
	
class Test(AuditModel):
	"""
	Test
	"""
	name=models.CharField(max_length=50, default=now_to_string())
	description=models.CharField(max_length=200, blank=True, null=True)
	
class Quiz(AuditModel):
	"""
	Quiz
	"""
	question=models.CharField(max_length=200, blank=True, null=True)
	answer1=models.CharField(max_length=50, blank=True, null=True)
	answer2=models.CharField(max_length=50, blank=True, null=True)
	answer3=models.CharField(max_length=50, blank=True, null=True)
	vocabulary=models.ForeignKey(Vocabulary, on_delete=models.CASCADE)
	correct_answer=models.CharField(max_length=50, blank=True, null=True)
	question_type=models.CharField(max_length=50, choices=QuizType.choices, default=QuizType.FIND_MEANING)
	
class QuizContent(AuditModel):
	"""
	QuizContent
	"""
	test=models.ForeignKey(Test, on_delete=models.CASCADE, related_name='test_content')
	quiz=models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz_content')