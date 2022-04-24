
from django.db import models
from datetime import date

def now_to_string():
    return date.today().strftime('%Y-%m-%d')

class AuditModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        abstract = True

class Word( AuditModel):
    """
    Word
    """
    name = models.CharField(max_length=1000, unique=True)

    def __str__(self):
        return self.name



class Collection( AuditModel):
    """
    Collection
    """

    name = models.CharField(max_length=50, unique=True, default = now_to_string())
    description = models.CharField(max_length=200, blank=True, null=True)
    image = models.FileField(upload_to='image/', blank=True, null=True)

    def __str__(self):
        return self.name + ': ' + self.description


class Language(models.TextChoices):
    """
    Language
    """
    ENGLISH = 'en', 'English'
    VIETNAMESE = 'vi', 'Vietnamese'
    JAPANESE = 'ja', 'Japanese'
    KOREAN = 'ko', 'Korean'
    CHINESE = 'zh', 'Chinese'
    FRENCH = 'fr', 'French'
    SPANISH = 'es', 'Spanish'
    GERMAN = 'de', 'German'
    ITALIAN = 'it', 'Italian'
    RUSSIAN = 'ru', 'Russian'
    PORTUGUESE = 'pt', 'Portuguese'
    ARABIC = 'ar', 'Arabic'
    BULGARIAN = 'bg', 'Bulgarian'
    CZECH = 'cs', 'Czech'
    DANISH = 'da', 'Danish'
    DUTCH = 'nl', 'Dutch'
    FINNISH = 'fi', 'Finnish'
    GREEK = 'el', 'Greek'
    HUNGARIAN = 'hu', 'Hungarian'
    ICELANDIC = 'is', 'Icelandic'
    INDONESIAN = 'id', 'Indonesian'
    IRISH = 'ga', 'Irish'
    LATVIAN = 'lv', 'Latvian'
    LITHUANIAN = 'lt', 'Lithuanian'
    NORWEGIAN = 'no', 'Norwegian'
    POLISH = 'pl', 'Polish'
    PORTUGUESE_BRAZIL = 'pt-br', 'Portuguese (Brazil)'
    ROMANIAN = 'ro', 'Romanian'
    SLOVAK = 'sk', 'Slovak'
    SLOVENIAN = 'sl', 'Slovenian'
    SWEDISH = 'sv', 'Swedish'
    TURKISH = 'tr', 'Turkish'
    UKRAINIAN = 'uk', 'Ukrainian'
    WELSH = 'cy', 'Welsh'

class PartOfSpeech(models.TextChoices):
    NOUN = 'NOUN', 'Noun'
    VERB = 'VERB', 'Verb'
    ADJ = 'ADJ', 'Adjective'
    ADV = 'ADV', 'Adverb'
    PRON = 'PRON', 'Pronoun'
    CONJ = 'CONJ', 'Conjunction'
    DET = 'DET', 'Determiner'
    PREP = 'PREP', 'Preposition'
    NUM = 'NUM', 'Numeral'
    INTERJ = 'INTERJ', 'Interjection'
    PRT = 'PRT', 'Particle'
    X = 'X', 'Other'

class Vocabulary( AuditModel):
    """
    Vocabulary
    """

    word = models.ForeignKey(Word,related_name= 'word', on_delete=models.CASCADE)
    meaning = models.CharField(max_length=100)
    example = models.CharField(max_length=200)
    phonetic = models.CharField(max_length=100)
    audio = models.FileField(upload_to='audio/')
    pos = models.CharField(max_length=50, choices=PartOfSpeech.choices, default=PartOfSpeech.NOUN)
    collection = models.ManyToManyField(Collection, related_name='vocabulary')
    language = models.CharField(max_length=20, choices=Language.choices, default=Language.ENGLISH)

    class Meta:
        unique_together = ('word', 'phonetic', 'pos')


    def __str__(self):
        return self.word + ': ' + self.meaning + ': ' + self.example + ': ' + self.phonetic + ': ' + self.audio.name + ': ' + self.pos.name


class VocabularyCollection( AuditModel):
    """
    Vocabulary Collection
    """

    collection = models.ForeignKey(Collection, on_delete=models.CASCADE )
    vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('collection', 'vocabulary')


class Typing( AuditModel):
    """
    Typing
    """

    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    typingCount = models.IntegerField(default=0)

    def __str__(self):
        return self.word + ': ' + str(self.typingCount)



