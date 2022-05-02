from rest_framework import serializers
from study.models import (Lesson, LessonItem, LessonContent, Test, Quiz, QuizContent, QuizType)
from datetime import datetime
from entities.models import Vocabulary

class LessonSerializer(serializers.ModelSerializer):
	class Meta:
		model=Lesson
		fields=['id','name', 'description']

	def validate_name(self, value):
		if len(value) > 50:
			raise serializers.ValidationError('Name must be less than 50 characters')
		if len(value) < 3:
			raise serializers.ValidationError('Name must be at least 3 characters')
		return value

	def validate(self, data):
		request=self.context.get('request')
		if request:
			user=request.user
			name=data.get('name', None)
			instance=self.instance if self.instance else Lesson(id=-1)
			is_exists=Lesson.objects.filter(created_by=user, name=name)\
									.exclude(deleted_by=user).exclude(id=instance.id).exists();
			if is_exists:
				raise serializers.ValidationError('Lesson with this name already exists')
		return data

	def save (self, **kwargs):
		return super(LessonSerializer, self).save(**kwargs)
	
	def update(self, instance, data):
		instance.name=data.get('name', instance.name)
		instance.description=data.get('description', instance.description)
		instance.updated_by=self.context.get('request').user
		instance.updated_at=datetime.now()
		instance.save()
		return instance
	
class LessonItemSerializer(serializers.ModelSerializer):
	class Meta:
		model=LessonItem
		fields=['id','vocabulary', 'typing_count', 'right_count', 'wrong_list']
	
	def validate_vocabulary(self, value):
		user=self.context.get('request').user
		vocabulary_exists=Vocabulary.objects.filter(id=value.id, deleted_by=None).exists()
		if vocabulary_exists and value.created_by == user:
			return value
		raise serializers.ValidationError('Vocabulary is not exists or you are not owner')
 
	def validate(self, data):
		request=self.context.get('request')
		if request:
			user=request.user
			vocabulary=data.get('vocabulary', None)
			instance=self.instance if self.instance else LessonItem(id=-1)
			is_exists=LessonItem.objects.filter(created_by=user, vocabulary=vocabulary)\
										.exclude(deleted_by=user).exclude(id=instance.id).exists();
			if is_exists:
				raise serializers.ValidationError('Vocabulary is already exists')
		return data

	def save(self, **kwargs):
			return super(LessonItemSerializer, self).save(**kwargs)
		
	def update(self, instance, data):
		instance.typing_count=data.get('typing_count', instance.typing_count)
		instance.right_count=data.get('right_count', instance.right_count)
		instance.wrong_list=data.get('wrong_list', instance.wrong_list)
		instance.updated_by=self.context.get('request').user
		instance.updated_at=datetime.now()
		instance.save()
		return instance
	
class LessonContentSerializer(serializers.ModelSerializer):
	class Meta:
		model=LessonContent
		fields=['id','lesson', 'item']

	def validate_lesson(self, value):
		user=self.context.get('request').user
		lesson_exists=Lesson.objects.filter(id=value.id, deleted_by=None).exists()
		if lesson_exists and value.created_by == user:
			return value
		raise serializers.ValidationError('Lesson is not exists or you are not owner')

	def validate_item(self, value):
		user=self.context.get('request').user
		item_exists=LessonItem.objects.filter(id=value.id, deleted_by=None).exists()
		if item_exists and value.created_by == user:
			return value
		raise serializers.ValidationError('LessonItem not exists')

	def validate(self, data):
		lesson=data.get('lesson', None)
		item=data.get('item', None)
		user=self.context.get('request').user
		instance=self.instance if self.instance else LessonContent(id=-1)
		content_exists=LessonContent.objects.filter(lesson=lesson, item=item)\
											.exclude(deleted_by=user).exclude(id=instance.id).exists()
		if content_exists:
			raise serializers.ValidationError('LessonContent is already exists')
		return data

	def save(self, **kwargs):
		return super(LessonContentSerializer, self).save(**kwargs)
	
	def update(self, instance, data):	 
		return instance
		
class TestSerializer(serializers.ModelSerializer):
	class Meta:
		model=Test
		fields=['id','name', 'description']
		
	def validate_name(self, value):
		if len(value) > 50:
			raise serializers.ValidationError('Name must be less than 50 characters')
		if len(value) < 3:
			raise serializers.ValidationError('Name must be at least 3 characters')
		return value

	def validate(self, data):
		user=self.context.get('request').user
		name=data.get('name', None)
		instance=self.instance if self.instance else Test(id=-1)
		is_exists=Test.objects.filter(created_by=user, name=name)\
							.exclude(deleted_by=user).exclude(id=instance.id).exists();
		if is_exists:
			raise serializers.ValidationError('Test with this name already exists')
		return data

	def save(self, **kwargs):
		return super(TestSerializer, self).save(**kwargs)
		
	def update(self, instance, data):
		instance.name=data.get('name', instance.name)
		instance.description=data.get('description', instance.description)
		instance.updated_by=self.context.get('request').user
		instance.updated_at=datetime.now()
		instance.save()
		return instance
		
class QuizSerializer(serializers.ModelSerializer):
	class Meta:
		model=Quiz
		fields=['id', 'question', 'answer1', 'answer2', 'answer3', \
					'vocabulary', 'correct_answer', 'question_type']
		extra_kwargs={
			'question': {'read_only': True},
			'answer1': {'required': True},
			'answer2': {'required': True},
			'answer3': {'required': True},
			'vocabulary': {'required': True},
			'correct_answer': {'read_only': True},
			'question_type': {'required': False},
		}

	def validate_vocabulary(self, value):
		user=self.context.get('request').user
		vocabulary_exists=Vocabulary.objects.filter(id=value.id, deleted_by=None).exists()
		if vocabulary_exists and value.created_by == user:
			return value
		raise serializers.ValidationError('Vocabulary is not exists or you are not owner')

	def validate(self, data):
		vocabulary=data.get('vocabulary', None)
		question_type=data.get('question_type', None)
		print(question_type == QuizType.FIND_WORD)
		if question_type is not None and question_type == QuizType.FIND_WORD:
			data['question']='Find word has meaning of \'' + vocabulary.meaning + '\''
			data['correct_answer']=vocabulary.word
		else:
			data['question_type']=QuizType.FIND_MEANING
			data['question']='Find meaning of \'' + vocabulary.word + '\''
			data['correct_answer']=vocabulary.meaning

		user=self.context.get('request').user
		question=data.get('question', None)
		answer1=data.get('answer1', None)
		answer2=data.get('answer2', None)
		answer3=data.get('answer3', None)
		instance=self.instance if self.instance else Quiz(id=-1)
		quiz_exists=Quiz.objects.filter(vocabulary=vocabulary, created_by=user,\
									question=question, answer1=answer1,\
									answer2=answer2, answer3=answer3)\
									.exclude(deleted_by=user).exclude(id=instance.id).exists()
		if quiz_exists:
			raise serializers.ValidationError('Quiz is already exists')
		return data
		
	def save(self, **kwargs):
		return super(QuizSerializer, self).save(**kwargs)
	
	def update(self, instance, data):
		instance.answer1=data.get('answer1', instance.answer1)
		instance.answer2=data.get('answer2', instance.answer2)
		instance.answer3=data.get('answer3', instance.answer3)
		instance.updated_by=self.context.get('request').user
		instance.updated_at=datetime.now()
		instance.save()
		return instance
	
class QuizContentSerializer(serializers.ModelSerializer):
	class Meta:
		model=QuizContent
		fields=['id', 'quiz', 'test']
	
	def validate_test(self, value):
		user=self.context.get('request').user
		test_exists=Test.objects.filter(id=value.id, deleted_by=None).exists()
		if test_exists and value.created_by == user:
			return value
		raise serializers.ValidationError('Test is not exists or you are not owner')

	def validate_quiz(self, value):
		user=self.context.get('request').user
		quiz_exists=Quiz.objects.filter(id=value.id, deleted_by=None).exists()
		if quiz_exists and value.created_by == user:
			return value
		raise serializers.ValidationError('Quiz is not exists or you are not owner')

	def validate(self, data):
		test=data.get('test', None)
		quiz=data.get('quiz', None)
		user=self.context.get('request').user
		instance=self.instance if self.instance else QuizContent(id=-1)
		test_content_exists=QuizContent.objects.filter(quiz=quiz, test=test)\
											.exclude(deleted_by=user).exclude(id=instance.id).exists()
		if test_content_exists:
			raise serializers.ValidationError('Test is already exists')
		return data

	def save(self, **kwargs):
		return super(QuizContentSerializer, self).save(**kwargs)
	
	def update(self, instance, data):
		return instance