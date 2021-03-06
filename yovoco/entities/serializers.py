from datetime import datetime
from entities.models import Collection, Vocabulary
from rest_framework import serializers
import requests
from yovoco.constants import *
class CollectionSerializer(serializers.ModelSerializer):
	class Meta:
		model=Collection
		fields=[KEY_ID, KEY_NAME, KEY_DESCRIPTION, KEY_IMAGE]
	
	def validate_name(self, value):
		if len(value) > VALUE_NAME_MAX_LENGTH:
			raise serializers.ValidationError(MESSAGE_VALIDATION_NAME_MOST_CHAR)
		if len(value) < VALUE_NAME_MIN_LENGTH:
			raise serializers.ValidationError(MESSAGE_VALIDATION_NAME_LEAST_CHAR)
		return value

	def validate(self, data):
		request=self.context.get(KEY_REQUEST)
		if request:
			user=request.user
			name=data.get(KEY_NAME)
			instance=self.instance if self.instance else Collection(id=-1)
			is_exists=Collection.objects.filter(created_by=user, name=name)\
												.exclude(deleted_by=user).exclude(id=instance.id).exists();
			if is_exists:
				raise serializers.ValidationError(MESSAGE_COLLECTION_EXIST)
		return data
	
	def save(self, **kwargs):
		return super(CollectionSerializer, self).save(**kwargs)

	def update(self, instance, data):
		instance.name=data.get(KEY_NAME, instance.name)
		instance.description=data.get(KEY_DESCRIPTION, instance.description)
		instance.image=data.get(KEY_IMAGE, instance.image)
		instance.updated_by=self.context.get(KEY_REQUEST).user
		instance.updated_at=datetime.now()
		instance.save()
		return instance
		
class VocabularySerializer(serializers.ModelSerializer):
	class Meta:
		model=Vocabulary
		fields=(KEY_ID,KEY_WORD, KEY_MEANING, KEY_EXAMPLE, KEY_PHONETIC, KEY_AUDIO,\
			KEY_POS, KEY_LANGUAGE, KEY_COLLECTION, KEY_POS_EXTEND)
		extra_kwargs={
			KEY_ID: {KEY_READ_ONLY: True},
			KEY_WORD: {KEY_REQUIRED: True},
			KEY_POS_EXTEND: {KEY_READ_ONLY: False}
		}
	
	def validate_audio(self, value):
		audio=self.initial_data.get(KEY_AUDIO)
		if (not audio) or audio.endswith(VALUE_MP3_EXTEND) or audio.endswith(VALUE_WAV_EXTEND):
			return value
		raise serializers.ValidationError(MESSAGE_VALIDATION_AUDIO_EXTEND)

	def validate_word(self, value):
		if len(value) > VALUE_VALIDATION_WORD_MAX_LENGTH:
			raise serializers.ValidationError(MESSAGE_VALIDATION_WORD_MOST_CHAR)
		if len(value) < VALUE_VALIDATION_WORD_MIN_LENGTH:
			raise serializers.ValidationError(MESSAGE_VALIDATION_WORD_LEAST_CHAR)
		return value

	def validate_collection(self, value):
		user=self.context.get(KEY_REQUEST).user
		if not value:
			collection_name=datetime.now().strftime('%Y%m%d')
			collection_exists=Collection.objects.filter(created_by=user, name=collection_name)\
													.exclude(deleted_by=user).exists()
			if not collection_exists:
				value=Collection.objects.create(created_by=user, updated_by=user,  name=collection_name,\
											description =VALUE_DESCRIPTION_AUTOMATIC);
			else:
				value=Collection.objects.get(created_by=user, name=collection_name)
		else:
			collection_exists=Collection.objects.filter(id=value.id, created_by=user).exists()
			if value.created_by != user and not collection_exists:
				raise serializers.ValidationError(MESSAGE_COLLECTION_NOT_EXIST)
		return value

	def get_meaning(self, data, json_data):
		meaning=data.get(KEY_MEANING)
		if not meaning or meaning.strip() == VALUE_EMPTY_STRING:
			defines=list()
			for translator in json_data:
				meanings=translator.get(KEY_MEANINGS)
				for meaning in meanings:
					definitions=meaning.get(KEY_DEFINITIONS)
					for definition in definitions:
						define=definition.get(KEY_DEFINITION)
						if define:
							defines.append(define)
			return VALUE_NEW_LINE.join(defines)
		return meaning
	
	def get_example_and_pos(self, data, json_data):
		example=data.get(KEY_EXAMPLE)
		pos_extend=data.get(KEY_POS_EXTEND)
		if not example or example.strip() == VALUE_EMPTY_STRING:
			examples=list()
			poses=list()
			for translator in json_data:
				meanings=translator.get(KEY_MEANINGS)
				for meaning in meanings:
					pos=meaning.get(KEY_PART_OF_SPEECH)
					if pos:
						poses.append(pos)
					definitions=meaning.get(KEY_DEFINITIONS)
					for definition in definitions:
						example=definition.get(KEY_EXAMPLE)
						if example:
							examples.append(example)
			return VALUE_NEW_LINE.join(set(examples)), VALUE_COMMA.join(set(poses))
		return example, pos_extend

	def get_phonetic(self, data, json_data):
		phonetic=data.get(KEY_PHONETIC)
		if not phonetic or phonetic.strip() == VALUE_EMPTY_STRING:
			phonetics=list()
			for translator in json_data:
				phonetic=translator.get(KEY_PHONETIC)
				if phonetic:
					phonetics.append(phonetic)
			return VALUE_NEW_LINE.join(set(phonetics))
		return phonetic

	def get_audio(self, data, json_data):
		audio=data.get(KEY_AUDIO)
		if not audio or audio.strip() == VALUE_EMPTY_STRING:
			audios=list()
			for translator in json_data:
				phonetics=translator.get(KEY_PHONETICS)
				for phonetic in phonetics:
					audio=phonetic.get(KEY_AUDIO)
					if audio:
						audios.append(audio)
			return VALUE_NEW_LINE.join(set(audios))
		return audio

	def validate (self, data):
		word=data.get(KEY_WORD)
		response=requests.get(DICTIONARY_API_URL.format(word))
		if response.status_code == 200:
			json_data: list=response.json()
			data[KEY_MEANING]=self.get_meaning(data, json_data)
			data[KEY_EXAMPLE], data[KEY_POS_EXTEND]=self.get_example_and_pos(data, json_data)
			data[KEY_PHONETIC]=self.get_phonetic(data, json_data)
			data[KEY_AUDIO]=self.get_audio(data, json_data)

		user=self.context.get(KEY_REQUEST).user
		new_instance=Vocabulary(created_by=user,id=-1)
		pos=data.get(KEY_POS, new_instance.pos)
		language=data.get(KEY_LANGUAGE, new_instance.language)
		collection_data=data.get(KEY_COLLECTION)
		collection=self.validate_collection(collection_data)
		instance=self.instance if self.instance else new_instance
		data[KEY_COLLECTION]=collection
		is_exists=Vocabulary.objects.filter(created_by_id=user, word=word,
												pos=pos, language=language, collection_id=collection)\
										.exclude(deleted_by=user).exclude(id=instance.id).exists();
		if is_exists:
			raise serializers.ValidationError(MESSSAGE_VOCABULARY_EXIST)
		return data

	def save(self, **kwargs):
		
		return super(VocabularySerializer, self).save(**kwargs)
	
	def update(self, instance, validated_data):
		instance.word=validated_data.get(KEY_WORD, instance.word)
		instance.meaning=validated_data.get(KEY_MEANING, instance.meaning)
		instance.example=validated_data.get(KEY_EXAMPLE, instance.example)
		instance.phonetic=validated_data.get(KEY_PHONETIC, instance.phonetic)
		instance.audio=validated_data.get(KEY_AUDIO, instance.audio)
		instance.pos=validated_data.get(KEY_POS, instance.pos)
		instance.language=validated_data.get(KEY_LANGUAGE, instance.language)
		instance.save()
		return instance