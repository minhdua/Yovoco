from django.db import models
from datetime import date
from users.models import CustomUser

def now_to_string():
	return date.today().strftime('%Y%m%d')

class AuditModel(models.Model):
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now=True)
	created_by=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(class)s_created_by')
	updated_by=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(class)s_updated_by')
	deleted_at=models.DateTimeField(blank=True, null=True)
	deleted_by=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(class)s_deleted_by')

	class Meta:
		abstract=True
		
class Collection( AuditModel):
	"""
	Collection
	"""
	name=models.CharField(max_length=50, default=now_to_string())
	description=models.CharField(max_length=200, blank=True, null=True)
	image=models.FileField(upload_to='image/', blank=True, null=True)

class Language(models.TextChoices):
	"""
	Language
	"""
	ENGLISH='en', 'English'
	VIETNAMESE='vi', 'Vietnamese'
	JAPANESE='ja', 'Japanese'
	KOREAN='ko', 'Korean'
	CHINESE='zh', 'Chinese'
	FRENCH='fr', 'French'
	SPANISH='es', 'Spanish'
	GERMAN='de', 'German'
	ITALIAN='it', 'Italian'
	RUSSIAN='ru', 'Russian'
	PORTUGUESE='pt', 'Portuguese'
	ARABIC='ar', 'Arabic'
	BULGARIAN='bg', 'Bulgarian'
	CZECH='cs', 'Czech'
	DANISH='da', 'Danish'
	DUTCH='nl', 'Dutch'
	FINNISH='fi', 'Finnish'
	GREEK='el', 'Greek'
	HUNGARIAN='hu', 'Hungarian'
	ICELANDIC='is', 'Icelandic'
	INDONESIAN='id', 'Indonesian'
	IRISH='ga', 'Irish'
	LATVIAN='lv', 'Latvian'
	LITHUANIAN='lt', 'Lithuanian'
	NORWEGIAN='no', 'Norwegian'
	POLISH='pl', 'Polish'
	PORTUGUESE_BRAZIL='pt-br', 'Portuguese (Brazil)'
	ROMANIAN='ro', 'Romanian'
	SLOVAK='sk', 'Slovak'
	SLOVENIAN='sl', 'Slovenian'
	SWEDISH='sv', 'Swedish'
	TURKISH='tr', 'Turkish'
	UKRAINIAN='uk', 'Ukrainian'
	WELSH='cy', 'Welsh'

class PartOfSpeech(models.TextChoices):
	NOUN='noun'
	VERB='verb'
	ADJ='adjective'
	ADV='adverb'
	PRON='pronoun'
	CONJ='conjunction'
	DET='determiner'
	PREP='preposition'
	NUM='numeral'
	INTERJ='interjection'
	PRT='particle'
	X='other'

class Vocabulary( AuditModel):
	"""
	Vocabulary
	"""
	word=models.CharField(max_length=255)
	meaning=models.CharField(max_length=100, blank=True, null=True)
	example=models.CharField(max_length=2000, blank=True, null=True)
	phonetic=models.CharField(max_length=1000, blank=True, null=True)
	audio=models.CharField(max_length=1000, blank=True, null=True)
	pos=models.CharField(max_length=50, choices=PartOfSpeech.choices, default=PartOfSpeech.NOUN)
	language=models.CharField(max_length=20, choices=Language.choices, default=Language.ENGLISH)
	collection=models.ForeignKey(Collection, on_delete=models.CASCADE, \
											related_name='vocabulary', blank=True, null=True)
	pos_extend=models.CharField(max_length=1000, blank=True, null=True)