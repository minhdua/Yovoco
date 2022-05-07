from datetime import datetime
from secrets import choice
from statistics import quantiles
from tkinter.messagebox import QUESTION
from entities.models import Vocabulary
from rest_framework import serializers
from study.models import (Lesson, LessonItem, LessonContent, Test, Quiz, QuizContent, QuizType)
from yovoco.constants import *
from yovoco.utils import get_not_null_or_default
import random, uuid
class LessonSerializer(serializers.ModelSerializer):
	class Meta:
		model=Lesson
		fields=[KEY_ID,KEY_NAME, KEY_DESCRIPTION]

	def validate_name(self, value):
		if len(value) > VALUE_NAME_MAX_LENGTH:
			raise serializers.ValidationError(MESSAGE_VALIDATION_NAME_LEAST_CHAR)
		if len(value) < VALUE_NAME_MIN_LENGTH:
			raise serializers.ValidationError(MESSAGE_VALIDATION_NAME_MOST_CHAR)
		return value

	def validate(self, data):
		request=self.context.get(KEY_REQUEST)
		if request:
			user=request.user
			name=data.get(KEY_NAME)
			instance=self.instance if self.instance else Lesson(id=uuid.uuid4())
			is_exists=Lesson.objects.filter(created_by=user, name=name)\
									.exclude(deleted_by=user).exclude(id=instance.id).exists();
			if is_exists:
				raise serializers.ValidationError(MESSAGE_LESSON_EXIST)
		return data

	def save (self, **kwargs):
		return super(LessonSerializer, self).save(**kwargs)
	
	def update(self, instance, data):
		self.instance.name=data.get(KEY_NAME, instance.name)
		self.instance.description=data.get(KEY_DESCRIPTION, instance.description)
		self.instance.updated_by=self.context.get(KEY_REQUEST).user
		self.instance.updated_at=datetime.now()
		return super(LessonSerializer, self).update(self.instance, data)
	
class LessonItemSerializer(serializers.ModelSerializer):
	class Meta:
		model=LessonItem
		fields=[KEY_ID,KEY_VOCABULARY, KEY_TYPING_COUNT, KEY_RIGHT_COUNT, KEY_WRONG_LIST]
	
	def validate_vocabulary(self, value):
		user=self.context.get(KEY_REQUEST).user
		vocabulary_exists=Vocabulary.objects.filter(id=value.id, deleted_by=None).exists()
		if vocabulary_exists and value.created_by == user:
			return value
		raise serializers.ValidationError(MESSAGE_VOCABULARY_NOT_EXIST)
 
	def validate(self, data):
		request=self.context.get(KEY_REQUEST)
		if request:
			user=request.user
			vocabulary=data.get(KEY_VOCABULARY)
			instance=self.instance if self.instance else LessonItem(id=uuid.uuid4())
			is_exists=LessonItem.objects.filter(created_by=user, vocabulary=vocabulary)\
										.exclude(deleted_by=user).exclude(id=instance.id).exists();
			if is_exists:
				raise serializers.ValidationError(MESSSAGE_VOCABULARY_EXIST)
		return data

	def save(self, **kwargs):
			return super(LessonItemSerializer, self).save(**kwargs)
		
	def update(self, instance, data):
		self.instance.typing_count=data.get(KEY_TYPING_COUNT, instance.typing_count)
		self.instance.right_count=data.get(KEY_RIGHT_COUNT, instance.right_count)
		self.instance.wrong_list=data.get(KEY_WRONG_LIST, instance.wrong_list)
		self.instance.updated_by=self.context.get(KEY_REQUEST).user
		self.instance.updated_at=datetime.now()
		return super(LessonItemSerializer, self).update(self.instance, data)
	
class LessonContentSerializer(serializers.ModelSerializer):
	class Meta:
		model=LessonContent
		fields=[KEY_ID,KEY_LESSON, KEY_ITEM]

	def validate_lesson(self, value):
		user=self.context.get(KEY_REQUEST).user
		lesson_exists=Lesson.objects.filter(id=value.id, deleted_by=None).exists()
		if lesson_exists and value.created_by == user:
			return value
		raise serializers.ValidationError(MESSAGE_LESSON_NOT_EXIST)

	def validate_item(self, value):
		user=self.context.get(KEY_REQUEST).user
		item_exists=LessonItem.objects.filter(id=value.id, deleted_by=None).exists()
		if item_exists and value.created_by == user:
			return value
		raise serializers.ValidationError(MESSAGE_LESSON_ITEM_NOT_EXIST)

	def validate(self, data):
		lesson=data.get(KEY_LESSON)
		item=data.get(KEY_ITEM,)
		user=self.context.get(KEY_REQUEST).user
		instance=self.instance if self.instance else LessonContent(id=uuid.uuid4())
		content_exists=LessonContent.objects.filter(lesson=lesson, item=item)\
											.exclude(deleted_by=user).exclude(id=instance.id).exists()
		if content_exists:
			raise serializers.ValidationError(MESSAGE_LESSON_CONTENT_EXIST)
		return data

	def save(self, **kwargs):
		return super(LessonContentSerializer, self).save(**kwargs)
	
	def update(self, instance, data):	 
		return self.instance
		
class TestSerializer(serializers.ModelSerializer):
	class Meta:
		model=Test
		fields=[KEY_ID,KEY_NAME, KEY_DESCRIPTION]
		
	def validate_name(self, value):
		if len(value) > VALUE_NAME_MAX_LENGTH:
			raise serializers.ValidationError(MESSAGE_VALIDATION_NAME_MOST_CHAR)
		if len(value) < VALUE_NAME_MIN_LENGTH:
			raise serializers.ValidationError(MESSAGE_VALIDATION_NAME_LEAST_CHAR)
		return value

	def validate(self, data):
		user=self.context.get(KEY_REQUEST).user
		name=data.get(KEY_NAME)
		instance=self.instance if self.instance else Test(id=uuid.uuid4())
		is_exists=Test.objects.filter(created_by=user, name=name)\
							.exclude(deleted_by=user).exclude(id=instance.id).exists();
		if is_exists:
			raise serializers.ValidationError(MESSAGE_TEST_EXIST)
		return data

	def save(self, **kwargs):
		return super(TestSerializer, self).save(**kwargs)
		
	def update(self, instance, data):
		self.instance.name=data.get(KEY_NAME, instance.name)
		self.instance.description=data.get(KEY_DESCRIPTION, instance.description)
		self.instance.updated_by=self.context.get(KEY_REQUEST).user
		self.instance.updated_at=datetime.now()
		return super(TestSerializer, self).update(self.instance, data)
		
class QuizSerializer(serializers.ModelSerializer):
	class Meta:
		model=Quiz
		fields=[KEY_ID, KEY_ANSWER1, KEY_ANSWER2, KEY_ANSWER3, \
				KEY_CORRECT_ANSWER, KEY_QUESTION_TYPE]
		extra_kwargs={
			KEY_ANSWER1: {KEY_ALLOW_NULL: True},
			KEY_ANSWER2: {KEY_ALLOW_NULL: True},
			KEY_ANSWER3: {KEY_ALLOW_NULL: True},
			KEY_CORRECT_ANSWER: {KEY_ALLOW_NULL: True},
			KEY_QUESTION_TYPE: {KEY_ALLOW_NULL: True}
		}

	def get_question_type_random(self):
		types = QuizType.members()
		return random.choice(types)

	def get_correct_answer_random(self):
		vocabularies = Vocabulary.objects.filter(deleted_by=None).all()
		vocabulary = random.choice(vocabularies)
		return vocabulary

	def get_answer_random(self, data):
		correct_answer = data[KEY_CORRECT_ANSWER]
		answer1 = get_not_null_or_default(data.get(KEY_ANSWER1), Vocabulary(id=uuid.uuid4()))
		answer2 = get_not_null_or_default(data.get(KEY_ANSWER2), Vocabulary(id=uuid.uuid4()))
		answer3 = get_not_null_or_default(data.get(KEY_ANSWER3), Vocabulary(id=uuid.uuid4()))

		vocabularies_filter = Vocabulary.objects.filter(pos=correct_answer.pos).exclude(id=correct_answer.id).exclude(id=answer1.id)\
										.exclude(id=answer2.id).exclude(id=answer3.id).all()
		answers_random = [v for v in vocabularies_filter]
		try:
			return random.choice(answers_random)
		except IndexError:
			return None

	def validate(self, data):
		"""Validate Data

		Args:
			data (Quiz): answer1, answer2, answer3, vocabulary, question_type

		Returns:
			Quiz: if data is valid return data else return data with random quesion or answer
		"""
		user=self.context.get(KEY_REQUEST).user
		question_type=data[KEY_QUESTION_TYPE]=data.get(KEY_QUESTION_TYPE, self.get_question_type_random())
		correct_answer=data[KEY_CORRECT_ANSWER]=get_not_null_or_default(data.get(KEY_CORRECT_ANSWER),self.get_correct_answer_random())
		answer1=data[KEY_ANSWER1]=get_not_null_or_default(data.get(KEY_ANSWER1), self.get_answer_random(data))
		answer2=data[KEY_ANSWER2]=get_not_null_or_default(data.get(KEY_ANSWER2), self.get_answer_random(data))
		answer3=data[KEY_ANSWER3]=get_not_null_or_default(data.get(KEY_ANSWER3), self.get_answer_random(data))
		answers=[answer1, answer2, answer3]
		answers.sort(key=lambda x: x.id)
		instance=self.instance if self.instance else Quiz(id=uuid.uuid4())
		quiz_find=Quiz.objects.filter(correct_answer=correct_answer, created_by=user, answer1=answers[0],\
									answer2=answers[1], answer3=answers[2], question_type=question_type)\
									.exclude(deleted_by=user).exclude(id=instance.id)
		if quiz_find.exists():
			self.instance = quiz_find.first()
		return data
		
	def save(self, **kwargs):
		try:
			return super(QuizSerializer, self).save(**kwargs)
		except Exception:
			return {KEY_MESSAGE: MESSAGE_QUIZ_EXIST}
	
	def update(self, instance, data):
		self.instance.answer1=data.get(KEY_ANSWER1, instance.answer1)
		self.instance.answer2=data.get(KEY_ANSWER2, instance.answer2)
		self.instance.answer3=data.get(KEY_ANSWER3, instance.answer3)
		self.instance.correct_answer=data.get(KEY_CORRECT_ANSWER, instance.correct_answer)
		self.instance.question_type=data.get(KEY_QUESTION_TYPE, instance.question_type)
		self.instance.updated_by=self.context.get(KEY_REQUEST).user
		self.instance.updated_at=datetime.now()
		self.instance.save()
		return self.instance
	
class QuizContentSerializer(serializers.ModelSerializer):
	class Meta:
		model=QuizContent
		fields=[KEY_ID, KEY_QUIZ, KEY_TEST]
	
	def validate_test(self, value):
		user=self.context.get(KEY_REQUEST).user
		test_exists=Test.objects.filter(id=value.id, deleted_by=None).exists()
		if test_exists and value.created_by == user:
			return value
		raise serializers.ValidationError(MESSAGE_TEST_NOT_EXIST)

	def validate_quiz(self, value):
		user=self.context.get(KEY_REQUEST).user
		quiz_exists=Quiz.objects.filter(id=value.id, deleted_by=None).exists()
		if quiz_exists and value.created_by == user:
			return value
		raise serializers.ValidationError(MESSAGE_QUIZ_NOT_EXIST)

	def validate(self, data):
		test=data.get(KEY_TEST)
		quiz=data.get(KEY_QUIZ)
		user=self.context.get(KEY_REQUEST).user
		instance=self.instance if self.instance else QuizContent(id=uuid.uuid4())
		test_content_exists=QuizContent.objects.filter(quiz=quiz, test=test)\
											.exclude(deleted_by=user).exclude(id=instance.id).exists()
		if test_content_exists:
			raise serializers.ValidationError(MESSAGE_TEST_CONTENT_EXIST)
		return data

	def save(self, **kwargs):
		return super(QuizContentSerializer, self).save(**kwargs)
	
	def update(self, instance, data):
		return self.instance

class QuizDTO:
	def __init__(self, id, question, choice1, choice2, choice3, choice4):
		self.id=id
		self.question=question
		self.choice1=choice1
		self.choice2=choice2
		self.choice3=choice3
		self.choice4=choice4

def get_quiz_dto(quiz):
	question_type = quiz.get(KEY_QUESTION_TYPE)
	answer1 = Vocabulary.objects.get(id=quiz.get(KEY_ANSWER1))
	answer2 = Vocabulary.objects.get(id=quiz.get(KEY_ANSWER2))
	answer3 = Vocabulary.objects.get(id=quiz.get(KEY_ANSWER3))
	correct_answer = Vocabulary.objects.get(id=quiz.get(KEY_CORRECT_ANSWER))

	choices = [answer1, answer2, answer3, correct_answer]
	random.shuffle(choices)
	if (question_type == QuizType.FIND_WORD):
		question = QuizType.FIND_WORD.label.format(correct_answer.meaning)
		choice1 = choices[0].word
		choice2 = choices[1].word
		choice3 = choices[2].word
		choice4 = choices[3].word
	else:
		question = QuizType.FIND_MEANING.label.format(correct_answer.word)
		choice1 = choices[0].meaning
		choice2 = choices[1].meaning
		choice3 = choices[2].meaning
		choice4 = choices[3].meaning
	return QuizDTO(quiz.get(KEY_ID), question, choice1, choice2, choice3, choice4).__dict__