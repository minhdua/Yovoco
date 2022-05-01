from calendar import c
from tkinter import E
from rest_framework import serializers
from entities.models import Collection, Vocabulary
import requests
from datetime import datetime

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name', 'description', 'image']
    
    def validate_name(self, value):
        if len(value) > 50:
            raise serializers.ValidationError('Name is too long')
        return value
    
    def save(self, **kwargs):
        request = self.context.get('request')
        if request:
            user = request.user
            is_exists = Collection.objects.filter(created_by_id=user, name=self.validated_data['name']).exists();
            if is_exists:
                raise serializers.ValidationError('Collection with this name already exists')
        return super(CollectionSerializer, self).save(**kwargs)
    
    def update(self, instance, data):
        instance.name = data.get('name', instance.name)
        instance.description = data.get('description', instance.description)
        instance.image = data.get('image', instance.image)
        instance.updated_by = self.context.get('request').user
        instance.updated_at = datetime.now()
        instance.save()
        return instance
        
class VocabularySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vocabulary
        fields = ('id','word', 'meaning', 'example', 'phonetic', 'audio', 'pos', 'language', 'collection','pos_extend')
        extra_kwargs = {
            'id': {'read_only': True},
            'word': {'required': True},
            'pos_extend': {'read_only': False}
        }
    
    def validate_audio(self, value):
        audio =  self.initial_data.get('audio', None)
        if (not audio)  or audio.endswith('.mp3') or audio.endswith('.wav'):
            return value
        raise serializers.ValidationError('Audio file must be .mp3 or .wav')
    
    def validate (self, data):
        response = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en/{}'.format(data['word']))
        if response.status_code == 200:
            json_data: list = response.json()
            
            meaning = data.get('meaning', None)
            if meaning is None or meaning.strip() == '':
                defines = list()
                for translator in json_data:
                     meanings = translator.get('meanings')
                     for meaning in meanings:
                        definitions = meaning.get('definitions')
                        for definition in definitions:
                            define = definition.get('definition')
                            if define:
                                defines.append('- '+define)
                data['meaning'] = '\n'.join(defines)
                                
            
            
            example = data.get('example', None)
            if example is None or example.strip() == '':
                examples = list()
                poses = list()
                for translator in json_data:
                     meanings = translator.get('meanings')
                     for meaning in meanings:
                        pos = meaning.get('partOfSpeech')
                        if pos:
                            poses.append(pos)
                        definitions = meaning.get('definitions')
                        for definition in definitions:
                            example = definition.get('example')
                            if example:
                                examples.append('- '+example)
                data['example'] = '\n'.join(set(examples))
                data['pos_extend'] = ','.join(set(poses))
                
            phonetic = data.get('phonetic', None)
            if phonetic is None or phonetic.strip() == '':
                phonetics = list()
                for  translator in json_data:
                    phonetic = translator.get('phonetic',None)
                    if phonetic:
                        phonetics.append('- '+phonetic)
                data['phonetic'] = '\n'.join(set(phonetics))
                
            audio = data.get('audio', None)
            if audio is None or audio.strip() == '':
                audios = list()
                for translator in json_data:
                    phonetics = translator.get('phonetics')
                    for phonetic in phonetics:
                        audio = phonetic.get('audio',None)
                        if audio:
                            audios.append('- '+audio)
                data['audio'] = '\n'.join(set(audios))
    
        collection = data.get('collection', None)
        if collection is None:
            collection_name = datetime.now().strftime('%Y%m%d')
            user = self.context.get('request').user
            collection = Collection.objects.get_or_create(created_by_id=user.id, updated_by_id=user.id, name=collection_name)[0];
            data['collection'] = collection
        return  data

    def save(self, **kwargs):
        request = self.context.get('request')
        if request:
            user = request.user
            new_instance = Vocabulary(created_by_id=user.id)
            
            is_collection_owner = Collection.objects.filter(created_by_id=user.id, id=self.validated_data['collection'].id, deleted_by_id=None).exists()
           
            if not is_collection_owner:
                raise serializers.ValidationError('Collection not exists or you are not owner')
             
            is_exists = Vocabulary.objects.filter(created_by_id=user.id, 
                                                  word=self.validated_data['word'], 
                                                  pos=self.validated_data.get('pos',new_instance.pos),
                                                  language=self.validated_data.get('language',new_instance.language),
                                                  collection_id=self.validated_data['collection']).exists();
            if is_exists:
                raise serializers.ValidationError('Vocabulary with this word already exists')
        
        return super(VocabularySerializer, self).save(**kwargs)
    
    def update(self, instance, validated_data):
        instance.word = validated_data.get('word', instance.word)
        instance.meaning = validated_data.get('meaning', instance.meaning)
        instance.example = validated_data.get('example', instance.example)
        instance.phonetic = validated_data.get('phonetic', instance.phonetic)
        instance.audio = validated_data.get('audio', instance.audio)
        instance.pos = validated_data.get('pos', instance.pos)
        instance.language = validated_data.get('language', instance.language)
        instance.collection_id = validated_data.get('collection', instance.collection_id)
        instance.save()
        return instance