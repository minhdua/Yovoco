from rest_framework import serializers
from study.models import (Lesson, LessonItem, LessonContent, Test, Quiz, QuizContent, QuizType)
from datetime import datetime
from entities.models import Vocabulary

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id','name', 'description']
        
    def save (self, **kwargs):
        request = self.context.get('request')
        if request:
            user = request.user
            is_exists = Lesson.objects.filter(created_by_id=user, name=self.validated_data['name']).exclude(deleted_by=self.context['request'].user).exists();
            if is_exists:
                raise serializers.ValidationError('Lesson with this name already exists')
        return super(LessonSerializer, self).save(**kwargs)
    
    def update(self, instance, data):
        instance.name = data.get('name', instance.name)
        instance.description = data.get('description', instance.description)
        instance.updated_by = self.context.get('request').user
        instance.updated_at = datetime.now()
        instance.save()
        return instance
    
        
class LessonItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonItem
        fields = ['id','vocabulary', 'typing_count', 'right_count', 'wrong_list']
        
    def save(self, **kwargs):
        vocabulary = self.validated_data['vocabulary']
        vocabulary_exists = Vocabulary.objects.filter(id=vocabulary.id, deleted_by_id=None).exists()
        if vocabulary.created_by != self.context['request'].user or not vocabulary_exists:
            raise serializers.ValidationError('Vocabulary is not exists or you are not owner')
        item_exists = LessonItem.objects.filter(vocabulary=vocabulary, created_by=self.context['request'].user).exclude(deleted_by=self.context['request'].user).exists()
        if item_exists:
            raise serializers.ValidationError('Vocabulary is already exists')
        return super(LessonItemSerializer, self).save(**kwargs)
    
    def update(self, instance, data):
        instance.typing_count = data.get('typing_count', instance.typing_count)
        instance.right_count = data.get('right_count', instance.right_count)
        instance.wrong_list = data.get('wrong_list', instance.wrong_list)
        instance.updated_by = self.context['request'].user
        instance.updated_at = datetime.now()
        instance.save()
        return instance
    
class LessonContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonContent
        fields = ['id','lesson', 'item']

    def save(self, **kwargs):
        
        lesson = self.validated_data['lesson']
        lesson_exists = Lesson.objects.filter(id=lesson.id, deleted_by_id=None).exists()
        if lesson.created_by != self.context['request'].user or not lesson_exists:
            raise serializers.ValidationError('Lesson not exists')
        
        item = self.validated_data['item']
        item_exists = LessonItem.objects.filter(id=item.id, deleted_by_id=None).exists()
        if item.created_by != self.context['request'].user or not item_exists:
            raise serializers.ValidationError('LessonItem not exists')
        
        
        content_exists = LessonContent.objects.filter(lesson=lesson, item=item).exclude(deleted_by=self.context['request'].user).exists()
        if content_exists:
            raise serializers.ValidationError('LessonContent is already exists')
    
        return super(LessonContentSerializer, self).save(**kwargs)
    
    def update(self, instance, data):     
        return instance
    
        
class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id','name', 'description']
        
    def save(self, **kwargs):
        request = self.context.get('request')
        if request:
            user = request.user
            is_exists = Test.objects.filter(created_by_id=user, name=self.validated_data['name']).exclude(deleted_by=self.context['request'].user).exists();
            if is_exists:
                raise serializers.ValidationError('Test with this name already exists')
        return super(TestSerializer, self).save(**kwargs)
        
    def update(self, instance, data):
        instance.name = data.get('name', instance.name)
        instance.description = data.get('description', instance.description)
        instance.updated_by = self.context.get('request').user
        instance.updated_at = datetime.now()
        instance.save()
        return instance
        
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'question', 'answer1', 'answer2', 'answer3', 'vocabulary', 'correct_answer', 'question_type']
        extra_kwargs = {
            'question': {'read_only': True},
            'answer1': {'required': True},
            'answer2': {'required': True},
            'answer3': {'required': True},
            'vocabulary': {'required': True},
            'correct_answer': {'read_only': True},
            'question_type': {'required': False},
        }
    def save(self, **kwargs):
        request = self.context.get('request')
        vocabulary = self.validated_data['vocabulary']
        print(vocabulary)
        vocabulary_exists = Vocabulary.objects.filter(id=vocabulary.id, deleted_by_id=None).exists()
        print(vocabulary_exists)
        if vocabulary.created_by != request.user or not vocabulary_exists:
            raise serializers.ValidationError('Vocabulary is not exists or you are not owner')
        
        question_type = self.validated_data.get('question_type', None)
        print(question_type== QuizType.FIND_MEANING)
        if question_type is None or question_type == QuizType.FIND_MEANING:
            self.validated_data['question'] = vocabulary.word
            self.validated_data['correct_answer'] = vocabulary.meaning
        else:
            self.validated_data['question'] = vocabulary.meaning
            self.validated_data['correct_answer'] = vocabulary.word
        
        quiz_exists = Quiz.objects.filter(vocabulary=vocabulary,
                                          question=self.validated_data['question'],
                                          answer1=self.validated_data['answer1'],
                                          answer2=self.validated_data['answer2'],
                                          answer3=self.validated_data['answer3'],
                                          created_by=request.user).exclude(deleted_by=self.context['request'].user).exists()
        if quiz_exists:
            raise serializers.ValidationError('Quiz is already exists')
        return super(QuizSerializer, self).save(**kwargs)
    
    def update(self, instance, data):
        instance.answer1 = data.get('answer1', instance.answer1)
        instance.answer2 = data.get('answer2', instance.answer2)
        instance.answer3 = data.get('answer3', instance.answer3)
        instance.updated_by = self.context.get('request').user
        instance.updated_at = datetime.now()
        instance.save()
        return instance
    
class QuizContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizContent
        fields = ['id', 'quiz', 'test']
        
    def save(self, **kwargs):
        test = self.validated_data['test']
        test_exists = Test.objects.filter(id=test.id, deleted_by_id=None).exists()
        if test.created_by != self.context['request'].user or not test_exists:
            raise serializers.ValidationError('Test not exists')
        quiz = self.validated_data['quiz']
        quiz_exists = Quiz.objects.filter(id=quiz.id, deleted_by_id=None).exists()
        if quiz.created_by != self.context['request'].user or not quiz_exists:
            raise serializers.ValidationError('Quiz not exists')
        test_content_exists = QuizContent.objects.filter(test_id=test.id, quiz_id=quiz.id)\
                                                .exclude(deleted_by=self.context['request'].user)\
                                                .exists()
        if test_content_exists:
            raise serializers.ValidationError('QuizContent is already exists')
        return super(QuizContentSerializer, self).save(**kwargs)
    
    def update(self, instance, data):
        return instance