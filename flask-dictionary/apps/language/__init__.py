# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Blueprint
from apps.database.models import LocalLanguage
blueprint = Blueprint(
    'languages_blueprint',
    __name__,
    url_prefix='/language'
)

languages=[
    {
        'language_code': 'GK',
        'language_name': 'Gikuyu',
        'active': True,
        'description': 'Language spoken in cental parts of Kenya'
    }
]

def add_all_languages():
    for lang in languages:
        l=LocalLanguage.objects(language_code=lang['language_code']).first()
        if l:
            l.description=lang["description"]
            l.language_name=lang["language_name"]
            l.active=lang["active"]
            l.save()
        else:
            l=LocalLanguage(**lang)
            l.save()
