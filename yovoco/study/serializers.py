from datetime import datetime
from statistics import quantiles
from entities.models import Vocabulary
from rest_framework import serializers
from study.models import (Lesson, LessonItem, LessonContent, Test, Quiz, QuizContent, QuizType)
from yovoco.constants import *
import random
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
			instance=self.instance if self.instance else Lesson(id=-1)
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
			instance=self.instance if self.instance else LessonItem(id=-1)
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
		instance=self.instance if self.instance else LessonContent(id=-1)
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
		instance=self.instance if self.instance else Test(id=-1)
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
		fields=[KEY_ID, KEY_QUESTION, KEY_ANSWER1, KEY_ANSWER2, KEY_ANSWER3, \
					KEY_VOCABULARY, KEY_CORRECT_ANSWER, KEY_QUESTION_TYPE]
		extra_kwargs={
			KEY_QUESTION: {KEY_READ_ONLY: True},
			KEY_ANSWER1: {KEY_REQUIRED: False, KEY_ALLOW_NULL: True},
			KEY_ANSWER2: {KEY_REQUIRED: False, KEY_ALLOW_NULL: True},
			KEY_ANSWER3: {KEY_REQUIRED: False, KEY_ALLOW_NULL: True},
			KEY_VOCABULARY: {KEY_REQUIRED: True, KEY_ALLOW_NULL: True},
			KEY_CORRECT_ANSWER: {KEY_READ_ONLY: True},
			KEY_QUESTION_TYPE: {KEY_REQUIRED: True, KEY_ALLOW_NULL: True},
		}

	def validate_vocabulary(self, value):
		""" Validate vocabulary

		Args:
			value (vocabulary): vocabulary need test

		Raises:
			serializers.ValidationError: if vocabulary is empty
			serializers.ValidationError: if vocabulary is not exist

		Returns:
			vocabulary: vocabulary random if vocabulary is empty else return vocabulary exists or itself
		"""
		user=self.context.get(KEY_REQUEST).user
		if not value:
			vocabularies = Vocabulary.objects.filter(created_by=user, deleted_by=None)
			try:
				value = random.choice(vocabularies)
			except IndexError:
				raise serializers.ValidationError(MESSAGE_VALIDATION_VOCABULARIES_IS_EMPTY)
		vocabulary_filter=Vocabulary.objects.filter(created_by=user, id=value.id, deleted_by=None)
		if vocabulary_filter.exists():
			value = vocabulary_filter.first()
			return value
		raise serializers.ValidationError(MESSAGE_VOCABULARY_NOT_EXIST)

	def validate_question_type(self, value):
		if not value:
			types = QuizType.members()
			value = random.choice(types)
		return value

	def get_answer_random(self, data):
		vocabulary = data.get(KEY_VOCABULARY)
		answer1 = data.get(KEY_ANSWER1)
		answer2 = data.get(KEY_ANSWER2)
		answer3 = data.get(KEY_ANSWER3)
		question_type = data.get(KEY_QUESTION_TYPE)
		if question_type == QuizType.FIND_WORD:
			vocabularies_filter = Vocabulary.objects.filter(pos=vocabulary.pos).exclude(id=vocabulary.id).exclude(word=answer1)\
										.exclude(word=answer2).exclude(word=answer3)
			answers_random = [v.word for v in vocabularies_filter]
		else :
			vocabularies_filter = Vocabulary.objects.filter(pos=vocabulary.pos).exclude(id=vocabulary.id).exclude(meaning=answer1)\
										.exclude(meaning=answer2).exclude(meaning=answer3)
			answers_random = [v.meaning for v in vocabularies_filter]
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
		vocabulary=data.get(KEY_VOCABULARY)
		question_type=data.get(KEY_QUESTION_TYPE)
		if question_type == QuizType.FIND_WORD:
			data[KEY_QUESTION]=MESSAGE_FIND_WORD_HAS_MEANING.format(vocabulary.meaning)
			data[KEY_CORRECT_ANSWER]=vocabulary.word
		else:
			data[KEY_QUESTION_TYPE]=QuizType.FIND_MEANING
			data[KEY_QUESTION]=MESSAGE_FIND_MEANING_OF.format(vocabulary.word)
			data[KEY_CORRECT_ANSWER]=vocabulary.meaning

		user=self.context.get(KEY_REQUEST).user
		question=data.get(KEY_QUESTION)
		answer1=data[KEY_ANSWER1]=self.get_answer_random(data) if not data.get(KEY_ANSWER1) else data.get(KEY_ANSWER1)
		answer2=data[KEY_ANSWER2]=self.get_answer_random(data) if not data.get(KEY_ANSWER2) else data.get(KEY_ANSWER2)
		answer3=data[KEY_ANSWER3]=self.get_answer_random(data) if not data.get(KEY_ANSWER3) else data.get(KEY_ANSWER3)
		instance=self.instance if self.instance else Quiz(id=-1)
		quiz_find=Quiz.objects.filter(vocabulary=vocabulary, created_by=user,\
									question=question, answer1=answer1,\
									answer2=answer2, answer3=answer3)\
									.exclude(deleted_by=user).exclude(id=instance.id)
		if quiz_find.exists():
			self.instance = quiz_find.first()
		return data
		
	def save(self, **kwargs):
		try:
			print('instance',self.instance)
			return super(QuizSerializer, self).save(**kwargs)
		except Exception:
			return {KEY_MESSAGE: MESSAGE_QUIZ_EXIST}
	
	def update(self, instance, data):
		self.instance.answer1=data.get(KEY_ANSWER1, instance.answer1)
		self.instance.answer2=data.get(KEY_ANSWER2, instance.answer2)
		self.instance.answer3=data.get(KEY_ANSWER3, instance.answer3)
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
		instance=self.instance if self.instance else QuizContent(id=-1)
		test_content_exists=QuizContent.objects.filter(quiz=quiz, test=test)\
											.exclude(deleted_by=user).exclude(id=instance.id).exists()
		if test_content_exists:
			raise serializers.ValidationError(MESSAGE_TEST_CONTENT_EXIST)
		return data

	def save(self, **kwargs):
		return super(QuizContentSerializer, self).save(**kwargs)
	
	def update(self, instance, data):
		return self.instance