from django.db import models
from yovoco.models import AuditModel, Language, PartOfSpeech
from yovoco.utils import now_to_string
from yovoco.constants import *
import uuid
class Collection( AuditModel):
	"""
	Collection
	"""
	id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name=models.CharField(max_length=50, default=now_to_string())
	description=models.CharField(max_length=200, default=VALUE_DESCRIPTION_DEFAULT,blank=True, null=True)
	image=models.FileField(upload_to=IMAGE_DEFAULT_FOLDER, blank=True, null=True)
 
	class Meta:
		db_table=VALUE_COLLECTION_TABLE

class Vocabulary( AuditModel):
	"""
	Vocabulary
	"""
	word=models.CharField(max_length=255)
	meaning=models.CharField(max_length=2000, blank=True, null=True)
	example=models.CharField(max_length=2000, blank=True, null=True)
	phonetic=models.CharField(max_length=1000, blank=True, null=True)
	audio=models.CharField(max_length=1000, blank=True, null=True)
	pos=models.CharField(max_length=50, choices=PartOfSpeech.choices, default=PartOfSpeech.NOUN)
	language=models.CharField(max_length=20, choices=Language.choices, default=Language.ENGLISH)
	collection=models.ForeignKey(Collection, on_delete=models.CASCADE, \
											related_name=KEY_VOCABULARY, blank=True, null=True)
	pos_extend=models.CharField(max_length=1000, blank=True, null=True)
 
	class Meta:
		db_table=VALUE_VOCABULARY_TABLE