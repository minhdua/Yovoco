from rest_framework import serializers
from entities.models import Collection, Vocabulary
import requests
from datetime import datetime

class CollectionSerializer(serializers.ModelSerializer):
	class Meta:
		model=Collection
		fields=['id', 'name', 'description', 'image']
	
	def validate_name(self, value):
		if len(value) > 50:
			raise serializers.ValidationError('Name is too long')
		if len(value) < 3:
			raise serializers.ValidationError('Name is too short')
		return value
	
	def save(self, **kwargs):
		request=self.context.get('request')
		if request:
			user=request.user
			name=self.validated_data.get('name',None)
			is_exists=Collection.objects.filter(created_by=user, name=name)\
												.exclude(deleted_by=request.user).exists();
			if is_exists:
				raise serializers.ValidationError('Collection with this name already exists')
		return super(CollectionSerializer, self).save(**kwargs)
	
	def update(self, instance, data):
		instance.name=data.get('name', instance.name)
		instance.description=data.get('description', instance.description)
		instance.image=data.get('image', instance.image)
		instance.updated_by=self.context.get('request').user
		instance.updated_at=datetime.now()
		instance.save()
		return instance
		
class VocabularySerializer(serializers.ModelSerializer):
	class Meta:
		model=Vocabulary
		fields=('id','word', 'meaning', 'example', 'phonetic', 'audio', 'pos', 'language', 'collection','pos_extend')
		extra_kwargs={
			'id': {'read_only': True},
			'word': {'required': True},
			'pos_extend': {'read_only': False}
		}
	
	def validate_audio(self, value):
		audio=self.initial_data.get('audio', None)
		if (not audio) or audio.endswith('.mp3') or audio.endswith('.wav'):
			return value
		raise serializers.ValidationError('Audio file must be .mp3 or .wav')

	def validate_word(self, value):
		if len(value) > 50:
			raise serializers.ValidationError('Word is too long')
		if len(value) < 3:
			raise serializers.ValidationError('Word is too short')
		return value

	def validate_collection(self, value):
		user=self.context.get('request').user
		if value is None:
			collection_name=datetime.now().strftime('%Y%m%d')
			collection_exists=Collection.objects.filter(created_by=user, name=collection_name)\
													.exclude(deleted_by=user).exists()
			if not collection_exists:
				value=Collection.objects.create(created_by=user, updated_by=user,  name=collection_name,\
											description ='Collection created automatically');
			else:
				value=Collection.objects.get(created_by=user, name=collection_name)
		else:
			collection_exists=Collection.objects.filter(id=value.id, created_by=user).exists()
			if value.created_by != user and not collection_exists:
				raise serializers.ValidationError('Collection is not exists')
		return value

	def get_meaning(self, data, json_data):
		meaning=data.get('meaning', None)
		if meaning is None or meaning.strip() == '':
			defines=list()
			for translator in json_data:
				meanings=translator.get('meanings', None)
				for meaning in meanings:
					definitions=meaning.get('definitions', None)
					for definition in definitions:
						define=definition.get('definition', None)
						if define:
							defines.append('- ' + define)
			return '\n'.join(defines)
		return meaning
	
	def get_example_and_pos(self, data, json_data):
		example=data.get('example', None)
		pos_extend=data.get('pos_extend', None)
		if example is None or example.strip() == '':
			examples=list()
			poses=list()
			for translator in json_data:
				meanings=translator.get('meanings')
				for meaning in meanings:
					pos=meaning.get('partOfSpeech')
					if pos:
						poses.append(pos)
					definitions=meaning.get('definitions')
					for definition in definitions:
						example=definition.get('example')
						if example:
							examples.append(example)
			return '\n'.join(set(examples)), ','.join(set(poses))
		return example, pos_extend

	def get_phonetic(self, data, json_data):
		phonetic=data.get('phonetic', None)
		if phonetic is None or phonetic.strip() == '':
			phonetics=list()
			for translator in json_data:
				phonetic=translator.get('phonetic',None)
				if phonetic:
					phonetics.append(phonetic)
			return '\n'.join(set(phonetics))
		return phonetic

	def get_audio(self, data, json_data):
		audio=data.get('audio', None)
		if audio is None or audio.strip() == '':
			audios=list()
			for translator in json_data:
				phonetics=translator.get('phonetics')
				for phonetic in phonetics:
					audio=phonetic.get('audio',None)
					if audio:
						audios.append(audio)
			return '\n'.join(set(audios))
		return audio

	def validate (self, data):
		word=data.get('word', None)
		response=requests.get('https://api.dictionaryapi.dev/api/v2/entries/en/{}'.format(word))
		if response.status_code == 200:
			json_data: list=response.json()
			data['meaning']=self.get_meaning(data, json_data)
			data['example'], data['pos_extend']=self.get_example_and_pos(data, json_data)
			data['phonetic']=self.get_phonetic(data, json_data)
			data['audio']=self.get_audio(data, json_data)

		user=self.context.get('request').user
		new_instance=Vocabulary(created_by=user,id=-1)
		pos=data.get('pos', new_instance.pos)
		language=data.get('language', new_instance.language)
		collection_data=data.get('collection')
		collection=self.validate_collection(collection_data)
		instance=self.instance if self.instance else new_instance
		data['collection']=collection
		is_exists=Vocabulary.objects.filter(created_by_id=user, word=word,
												pos=pos, language=language, collection_id=collection)\
										.exclude(deleted_by=user).exclude(id=instance.id).exists();
		if is_exists:
			raise serializers.ValidationError('Vocabulary with this word already exists')
		return data

	def save(self, **kwargs):
		
		return super(VocabularySerializer, self).save(**kwargs)
	
	def update(self, instance, validated_data):
		instance.word=validated_data.get('word', instance.word)
		instance.meaning=validated_data.get('meaning', instance.meaning)
		instance.example=validated_data.get('example', instance.example)
		instance.phonetic=validated_data.get('phonetic', instance.phonetic)
		instance.audio=validated_data.get('audio', instance.audio)
		instance.pos=validated_data.get('pos', instance.pos)
		instance.language=validated_data.get('language', instance.language)
		instance.save()
		return instance