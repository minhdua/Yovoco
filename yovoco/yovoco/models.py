from django.db import models
from users.models import CustomUser

class AuditModel(models.Model):
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now=True)
	created_by=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(class)s_created_by')
	updated_by=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(class)s_updated_by')
	deleted_at=models.DateTimeField(blank=True, null=True)
	deleted_by=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(class)s_deleted_by')

	class Meta:
		abstract=True

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

class QuizType(models.TextChoices):
	"""
	QuizType
	"""
	FIND_MEANING='fm', 'Find Meaning'
	FIND_WORD='fw', 'Find Word'
	FIND_WORD_MEANING='fwm', 'Find Word and Meaning'
	FIND_WORD_FROM_IMAGE='fwi', 'Find Word from Image'
	FIND_WORD_FROM_AUDIO='fwa', 'Find Word from Audio'
	FIND_MEAN_FROM_IMAGE='fmi', 'Find Mean from Image'