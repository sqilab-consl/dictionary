from flask_login import UserMixin
import mongoengine as db
REVIEW_ROLES=[
    {
        'role':'level0_review',
        'name': 'New reviewers',
        'description': 'Can only submit words or recommend edits for review by other levels'
    },
    {
        'role':'level1_review',
        'name': 'Level 1 reviews',
        'description': 'First tiem reviews'
    },
    {
        'role':'semi_pro_review',
        'name': 'Semi Pro reviews',
        'description': 'Level two reviewers for profesional reviewers'
    },
    {
        'role':'profesional',
        'name': 'Profesional reviewers',
        'description': 'Profesional and language expert reviewers'
    },
]
# 0. Reviews
class ReviewStage(db.Document):
    stage_name=db.StringField(required=True)
    role=db.StringField(required=True)
    searchable=db.BooleanField(default=False)
    description=db.StringField(required=True)

# 1. Language Defination
class LocalLanguage(db.Document):
    language_name=db.StringField(required=True)
    language_code=db.StringField(required=True)
    active=db.BooleanField()
    description=db.StringField()
    meta={'collection': 'lexicons_languages'}

class LanguageLetters(db.Document):
    letter_index=db.IntField()
    category=db.StringField(required=True)
    letter=db.StringField(required=True)
    meta={'collection': 'lexicons_language_letters'}

# User Management
class Roles(db.Document):
    role_name=db.StringField(required=True)
    description=db.StringField(required=True)

class RoleAssignment(db.EmbeddedDocumentField):
    role_id=db.ReferenceField(Roles,required=True)
    language=db.ReferenceField(LocalLanguage,required=True)

class Users(UserMixin,db.Document):
    first_name=db.StringField(required=False)
    last_name=db.StringField(required=False)
    username=db.StringField(required=False)
    password=db.StringField(required=False)
    email_address=db.StringField(required=False)
    roles=db.ListField(RoleAssignment)
    is_active=db.BooleanField()
    meta = {
        'strict': False
        }
# Words
class WordForm(db.EmbeddedDocument):
    orthographic_form=db.StringField()
    pronunciation=db.StringField()
    hyphenation=db.StringField()
    syllabification=db.StringField()
    stress=db.StringField()
    label=db.StringField()
    part_of_speech=db.StringField()
    mood=db.StringField()
    meta={'collection': 'lexicons_wordform'}

# Grammar
class GrammarInformation(db.EmbeddedDocument):
    part_of_speech=db.StringField()
    mood=db.StringField()
# Other language translations
class Translations(db.EmbeddedDocument):
    translation_type=db.StringField()
    language=db.StringField()
    label=db.StringField()
    translation=db.StringField()
    quotation=db.StringField()

class TranslationExamples(db.EmbeddedDocument):
    translation_type=db.StringField()
    language=db.StringField()
    translation=db.StringField()
    quotation=db.StringField()
    meta={'collection': 'lexicons_translationexamples'}

class CitationExamples(db.EmbeddedDocument):
    translation_type=db.StringField() # example,translation
    citation=db.StringField()
    quotation=db.StringField()
    meta={'collection': 'lexicons_translationexamples'}

# Meanings
class WordSense(db.EmbeddedDocument):
    grammar_group = db.EmbeddedDocumentField(GrammarInformation) # GramGrp
    part_of_speech=db.StringField()
    subscript=db.StringField()
    pronunciation=db.StringField()
    defination=db.StringField()
    examples = db.EmbeddedDocumentListField(CitationExamples, default=[])
    meta={'collection': 'lexicons_wordsense'}
# Create your models here.
class WordEntry(db.Document):
    language=db.ReferenceField(LocalLanguage,required=True)
    word=db.StringField(required=True)
    year = db.IntField()
    month = db.IntField()
    forms = db.EmbeddedDocumentListField(WordForm)
    grammarGroup =db.EmbeddedDocumentField(GrammarInformation) # GramGrp
    meanings = db.EmbeddedDocumentListField(WordSense,default=[])
    translations = db.EmbeddedDocumentListField(Translations,default=[])
    meta={'collection': 'lexicons_wordentry'}

## 2. Phrases
class PhraseSense(db.EmbeddedDocument):
    mood = db.StringField()
    subscript=db.StringField()
    citation= db.StringField()
    defination=db.StringField()
    examples = db.EmbeddedDocumentListField(CitationExamples, default=[])
    meta={'collection': 'lexicons_wordsense'}

class WordPhraseEntry(db.Document):
    language=db.ReferenceField(LocalLanguage,required=True)
    phrase=db.StringField(required=True)
    category=db.StringField() # Saying, Proverbs, Idioms: Ref: https://www.smart-words.org/quotes-sayings/aphorism-proverb-idiom-saying-pun.html
    year = db.IntField()
    month = db.IntField()
    mood=db.StringField()
    author=db.StringField()
    meanings = db.EmbeddedDocumentListField(PhraseSense,default=[])
    examples = db.EmbeddedDocumentListField(CitationExamples,default=[])
    translations = db.EmbeddedDocumentListField(Translations,default=[])
    meta={'collection': 'language_phraseentry'}
