from apps.language import blueprint
from flask import render_template, request, url_for, redirect,jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound
from werkzeug.local import LocalProxy
from flask import current_app
from apps.database.models import LocalLanguage, WordEntry, WordForm,WordSense,WordPhraseEntry
from apps.language.forms import LocalLanguageForm,WordEntryForm, WordSenseForm, WordEntryTranslationForm, WordFormForm,PhraseForm,PhraseMeaningForm
from apps.language.service import *
logger = LocalProxy(lambda: current_app.logger)

def create_response(response_code,response_message, data=None, errors=None):
    return {
            'repsonse_code': response_code,
            'response_message': response_message,
            'errors': errors,
            'data': data
        }
@blueprint.route('/languages',methods=['GET'])
@login_required
def languages():
    logger.info("Languages")
    languages=LocalLanguage.objects()
    return render_template('language/languages.html', segment='language',languages=languages)

@blueprint.route('/add',methods=['GET','POST'])
@login_required
def add_language():
    lang_form=LocalLanguageForm(request.form)
    logger.info("Add Languages 1")
    if 'add_language' in request.form:
        logger.debug("Add Languages: 2")
        message=None
        if lang_form.validate():
            try:
                data=request.form.to_dict(flat=True)
                del data['add_language']
                del data['csrf_token']
                lang=LocalLanguage(**data)
                lang.save()
                return redirect(url_for('languages_blueprint.languages'), code=302)
            except Exception as ex:
                logger.error(ex)
                message="Failed to add record, please correct errors"
        else:
            message="Invalid details, please correct errors"
        return render_template('language/languageform.html', segment='language',form=lang_form,message=message)
    return render_template('language/languageform.html', segment='language',form=lang_form)

@blueprint.route('/words/<language>',methods=['GET'])
@login_required
def list_words(language):
    logger.info("Words: "+language)
    lang=LocalLanguage.objects(id=language).first()
    if lang is None:
        return redirect('blueprint.languages')
    phrases=WordEntry.objects(language=lang)
    return render_template('language/phrases.html', segment='phrases',language=lang, phrases=phrases)

@blueprint.route('/phrases/<language>',methods=['GET'])
@login_required
def list_phrases(language):
    logger.info("Words: "+language)
    lang=LocalLanguage.objects(id=language).first()
    if lang is None:
        return redirect('blueprint.languages')
    word_phrases=WordPhraseEntry.objects(language=lang)
    return render_template('language/phrases.html', segment='words',language=lang, phrases=word_phrases)

@blueprint.route('/phrases/<language>/view/<phrase_id>',methods=['GET'])
@login_required
def view_phrase(language, phrase_id):
    logger.info("Phrases: "+language)
    lang=LocalLanguage.objects(id=language).first()
    if lang is None:
        return redirect('blueprint.languages')
    phrase_details=WordPhraseEntry.objects(id=phrase_id,language=lang).first()
    print(phrase_details)
    return render_template('language/view_phrase.html', segment='view_phrase',language=lang, phrase=phrase_details)

@blueprint.route('/phrases/<language>/add',methods=['GET','POST','PATCH'])
@login_required
def add_phrase(language):
    logger.info("Add Phrases: "+language)
    lang=LocalLanguage.objects(id=language).first()
    if lang is None:
        return redirect('blueprint.languages')
    phrase_form=PhraseForm(request.form)
    errors={}
    if request.method=='POST':
        phrase,errors=add_update_word_phrase(phrase_form,lang)
        if len(errors)>0:
            return create_response("01","Failed to add phrase",errors=errors)
        else:
            return create_response("00","Success",data=phrase)
    return render_template('language/add_phrase.html', segment='add_phrase',language=lang,form=phrase_form, errors=errors)

@blueprint.route('/phrases/<language>/meaning/<phrase_id>/add',methods=['GET','POST','PATCH'])
@login_required
def add_word_phrase_meaning(language, phrase_id):
    logger.info("Phrases: "+language)
    lang=LocalLanguage.objects(id=language).first()
    if lang is None:
        return redirect('blueprint.languages')
    form=PhraseMeaningForm(request.form)
    if request.method in ['POST','PATCH']:
        phrase,errors=add_update_word_phrase_meaning(form,lang,phrase_id)
        if len(errors)>0:
            return create_response('01','Failed',errors=errors)
        else:
            return create_response('00','Success',data=phrase)
    else:
        phrase=WordPhraseEntry.objects(id=phrase_id,language=language).first()
    return render_template('language/add_word_phrase_meaning.html', segment='add_word_phrase_meaning',language=lang, form=form, phrase=phrase)

@blueprint.route('/words/<language>/add',methods=['GET','POST'])
@login_required
def add_language_word(language):
    logger.info("Add Words: "+language)
    errors={}
    lang_form=WordEntryForm(request.form)
    lang=LocalLanguage.objects(id=language).first()
    if request.method=='POST':
        if lang is None:
            errors['language']='Invalid language selected'
        else:
            lang_form,errors=add_update_word(lang_form,lang)
    return render_template('language/add_word.html', segment='add_language_word',form=lang_form,language=lang,errors=errors)

@blueprint.route('/words/<language>/meaning/<word_id>/view',methods=['GET','PUT','POST'])
@login_required
def view_language_word_meaning(language,word_id):
    logger.info("Update Words Meaning: "+language)
    errors={}
    lang_form=WordSenseForm(request.form)
    lang=LocalLanguage.objects(id=language).first()
    meanings=[]
    word=None
    if request.method=='PUT' or request.method=='POST':
        if lang is None:
            errors['language']='Invalid language selected'
        else:
            lang_form,errors=add_update_word(lang_form,lang)
    else:
        word=WordEntry.objects(id=word_id).first()
        if word is not None:
            meanings=word.meanings
        else:
            return redirect(url_for('languages_blueprint.list_words', language=lang.id), code=302)
    return render_template('language/view_word.html', segment='view_word_details',word=word,meanings=meanings,form=lang_form,language=lang,errors=errors)

@blueprint.route('/words/<language>/meaning/<word_id>/add',methods=['GET','PUT','POST'])
@login_required
def add_word_meaning(language,word_id):
    logger.info("Update Words Meaning: "+language)
    errors={}
    lang_form=WordSenseForm(request.form)
    lang=LocalLanguage.objects(id=language).first()
   
    word=WordEntry.objects(id=word_id).first()
    if word is None:
        return jsonify(create_response('01','Invalid selected word'))
    if request.method=='PUT' or request.method=='POST':
        if lang is None:
            errors['language']='Invalid language selected'
        else:
            word,errors=add_update_word_meaning(lang_form,lang, word)
        if len(errors)>0:
            return jsonify(create_response('02','Failed to add meaning', errors=errors))
        else:
            return jsonify(create_response('00','Success'))
    
    return render_template('language/word_meaning.html', segment='add_word_meaning',word=word,form=lang_form,language=lang,errors=errors)

@blueprint.route('/words/<language>/translation/<word_id>/add',methods=['GET','PUT','POST'])
@login_required
def add_word_translation(language,word_id):
    logger.info("Update Words Meaning: "+language)
    errors={}
    lang_form=WordEntryTranslationForm(request.form)
    lang=LocalLanguage.objects(id=language).first()
   
    word=WordEntry.objects(id=word_id).first()
    if word is None:
        return jsonify(create_response('01','Invalid selected word'))
    if request.method=='PUT' or request.method=='POST':
        if lang is None:
            errors['language']='Invalid language selected'
        else:
            word,errors=add_update_word_translation(lang_form, word)
        if len(errors)>0:
            return jsonify(create_response('02','Failed to add translation', errors=errors))
        else:
            return jsonify(create_response('00','Success'))
    
    return render_template('language/add_word_translation.html', segment='add_word_translation',word=word,form=lang_form,language=lang,errors=errors)

@blueprint.route('/words/<language>/forms/<word_id>/add',methods=['GET','PUT','POST'])
@login_required
def add_word_form(language,word_id):
    logger.info("Update Words Forms: "+language)
    errors={}
    lang_form=WordFormForm(request.form)
    lang=LocalLanguage.objects(id=language).first()
   
    word=WordEntry.objects(id=word_id).first()
    if word is None:
        return jsonify(create_response('01','Invalid selected word'))
    if request.method=='PUT' or request.method=='POST':
        if lang is None:
            errors['language']='Invalid language selected'
        else:
            word,errors=add_update_word_form(lang_form, word)
        if len(errors)>0:
            return jsonify(create_response('02','Failed to add translation', errors=errors))
        else:
            return jsonify(create_response('00','Success'))
    
    return render_template('language/add_word_form.html', segment='add_word_translation',word=word,form=lang_form,language=lang,errors=errors)