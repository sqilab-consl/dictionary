import json
import logging

from apps.database.models import LocalLanguage, WordEntry, WordForm,WordSense, GrammarInformation,CitationExamples, Translations, WordPhraseEntry,PhraseSense
from apps.language.forms import LocalLanguageForm,WordEntryForm,WordSenseForm, WordEntryTranslationForm,WordFormForm,PhraseForm, PhraseMeaningForm

def add_update_word(form: WordEntryForm, lang: LocalLanguage,word_id=None):
    errors={}
    word=WordEntry()
    word.year=form.year.data
    word.word=form.word.data.title()
    existing=WordEntry.objects(word=word.word, language=lang).first()
    if existing is not None:
        if word_id is None:
            errors['word']='Already exists'
        else:
            word=existing
            word.year=form.year.data
    if len(errors)==0:
        word.language=lang
        w=word.save()
    return form, errors

def add_update_word_meaning(form: WordSenseForm, lang: LocalLanguage,word,word_meaning_id=None):
    errors={}
    if word is None:
        errors['word']='Word does not exists'
    meaning=WordSense()
    if len(errors)==0:
        try:
            meaning.pronunciation=form.pronunciation.data
            meaning.part_of_speech=form.part_of_speach.data
            meaning.mood=form.mood.data
            meaning.subscript=form.subscript.data
            if len(form.mood.data)>0:
                gmer=GrammarInformation()
                gmer.part_of_speech=form.part_of_speach.data
                gmer.mood=form.mood.data
                meaning.grammar_group=gmer
            if len(form.example_sentence.data)>0:
                example=CitationExamples()
                example.citation=form.example_sentence.data
                example.translation_type='example'
                meaning.examples.append(example)
            word.meanings.append(meaning)
            print("Data: {}".format(word.to_mongo()))
            word=word.save()
        except Exception as ex:
            print(ex)
            errors['error']='Failed to update word, please try again'
    return word, errors

def add_update_word_translation(form: WordEntryTranslationForm,word,word_translation_id=None):
    errors={}
    if word is None:
        errors['word']='Word does not exists'
    translation=Translations()
    if len(errors)==0:
        try:
            translation.language=form.language.data
            translation.quotation=form.quotation.data
            translation.translation_type='translation'
            translation.translation=form.translation.data
            translation.label=form.example_statement.data
            if word.translations is None:
                word.translations=[]
            word.translations.append(translation)
            print("Data: {}".format(word.to_mongo()))
            word=word.save()
        except Exception as ex:
            print(ex)
            errors['error']='Failed to update word, please try again'
    return word, errors

def add_update_word_form(form: WordFormForm,word,word_translation_id=None):
    errors={}
    if word is None:
        errors['word']='Word does not exists'
    word_form=WordForm()
    if len(errors)==0:
        try:
            word_form.hyphenation=form.hyphenation.data
            word_form.label=form.word_label.data
            word_form.mood=form.mood.data
            word_form.orthographic_form=form.orthographic_form.data
            word_form.part_of_speech=form.part_of_speach.data
            word_form.pronunciation=form.pronunciation.data
            word_form.stress=form.stress.data
            word_form.syllabification=form.syllabification.data
            if word.forms is None:
                word.forms=[]
            word.forms.append(word_form)
            print("Data: {}".format(word.to_mongo()))
            word=word.save()
        except Exception as ex:
            logging.error("Failed to add word form", ex)
            errors['error']='Failed to update word, please try again'
    return word, errors


def add_update_word_phrase(form: PhraseForm,language,pharase_id=None):
    errors={}
    if language is None:
        errors['language']='Language does not exists'
    word_phrase=WordPhraseEntry()
    if len(errors)==0:
        try:
            word_phrase.phrase=form.phrase.data
            word_phrase.author=form.phrase.data
            word_phrase.year=form.year.data
            word_phrase.month=1
            word_phrase.language=language
            word_phrase.category=form.category.data
            word_phrase.mood=form.mood.data
            word=word_phrase.save()
        except Exception as ex:
            logging.error("Failed to add word form", ex)
            errors['error']='Failed to update word, please try again'
    return word_phrase, errors
def add_update_word_phrase_meaning(form: PhraseMeaningForm,language,phrase_id):
    errors={}
    if language is None:
        errors['language']='Language does not exists'
    phrase=WordPhraseEntry.objects(id=phrase_id,language=language).first()
    if phrase is None:
        errors['language']='Phrase is required'
    word_phrase_meaning=PhraseSense()
    if len(errors)==0:
        try:
            word_phrase_meaning.citation=form.citation.data
            word_phrase_meaning.defination=form.defination.data
            word_phrase_meaning.mood=form.mood.data
            word_phrase_meaning.subscript=form.subscript.data
            if phrase.meanings is None:
                phrase.meanings=[]
            phrase.meanings.append(word_phrase_meaning)
            # Add example
            if len(form.example_sentence.data)>0:
                example=CitationExamples()
                example.citation=''
                example.quotation=form.example_sentence.data
                example.translation_type='example'
                if phrase.examples is None:
                    phrase.examples=[]
                phrase.examples.append(example)
            # Save examples
            phrase=phrase.save()
        except Exception as ex:
            logging.error("Failed to add word form", ex)
            errors['error']='Failed to update word, please try again'
    return phrase, errors