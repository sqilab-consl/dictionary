from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, FieldList, FormField, IntegerField, SelectField
from wtforms.validators import Email, DataRequired
COMMON_LANGUAGES=[
    ("EN","English"),
    ("FR", "French"),
    ("GR","Gernman"),
    ("CN","Chinese"),
    ("SW","Swahili"),
    ("IT","Italian")
]
WORD_FORM_LABELS=[
    ('SYN',"Synonymn"),
    ('ABR',"Abreviation"),
    ('LIT',"Literal"),
    ('CONTR',"Contraction")
]
PARTS_OF_SPEACH=[
    ('ADVERB',"Adverb"),
    ('ADJECTIVE',"Adjective"),
    ('VERB',"Verb"),
    ('NOUN',"Noun"),
    ('PRONOUN',"Pronoun"),
    ('PREPOSITION',"Prepositions"),
    ('CONJUCTIONS', "Conjuctions"),
    ('ARTICLES',"Articles")
]
WORD_PHRASE_CATEGORIES=[
    ('PROVERB',"Proverbs"),
    ('SAYING','SAYING'),
    ('IDIOM','Idiom'),
    ('SLOGAN','Slogan'),
    ('PUN','Pun'),
    ('MOTTO','Motto'),
    ('HYPERBOLE','Hyperbole'),
    ('CLICHE','Cliché')
]
class LocalLanguageForm(FlaskForm):
    language_name=StringField()
    language_code=StringField()
    active=BooleanField()
    description=StringField()

class WordEntryTranslationForm(FlaskForm):
    language=SelectField(choices=COMMON_LANGUAGES)
    translation=StringField()
    quotation=StringField()
    example_statement=StringField()
    active=BooleanField()

class WordSenseForm(FlaskForm):
    # Grammer info
    part_of_speach=SelectField(choices=PARTS_OF_SPEACH)
    mood=StringField()
    # Meaning
    subscript=StringField()
    pronunciation=StringField()
    defination=StringField()
    example_sentence=StringField()

class WordFormForm(FlaskForm):
    orthographic_form=StringField()
    pronunciation=StringField()
    hyphenation=StringField()
    syllabification=StringField()
    stress=StringField()
    word_label=SelectField(choices=WORD_FORM_LABELS)
    part_of_speach=SelectField(choices=PARTS_OF_SPEACH)
    mood=StringField()

class WordEntryForm(FlaskForm):
    word=StringField()
    year=IntegerField()
# Phrases
class PhraseForm(FlaskForm):
    phrase=StringField()
    category=SelectField(choices=WORD_PHRASE_CATEGORIES) # Saying, Proverbs, Idioms: Ref: https://www.smart-words.org/quotes-sayings/aphorism-proverb-idiom-saying-pun.html
    author=StringField()
    mood=StringField()
    year = IntegerField()
class PhraseMeaningForm(FlaskForm):
    citation=StringField()
    mood=StringField()
    subscript=StringField()
    defination = StringField()
    example_sentence=StringField()