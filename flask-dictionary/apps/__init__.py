# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Flask
from flask_login import LoginManager
from importlib import import_module
from apps.language import add_all_languages
from .database import initialize_database
login_manager = LoginManager()


def register_extensions(app):
    app.logger.info('INIT login manager')
    login_manager.init_app(app)


def register_blueprints(app):
    for module_name in ('authentication','language', 'home','users'):
        app.logger.info('Routes Register {}'.format(module_name))
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)
    app.logger.info([str(p) for p in app.url_map.iter_rules()])

def configure_database(app):
    app.logger.info('INTI database..')
    initialize_database(app)
    add_all_languages()


def create_app(config):
    app = Flask(__name__)
    if config:
        app.config.from_object(config)
    app.logger.info('INIT application')
    register_extensions(app)
    register_blueprints(app)
    # connect to the database
    app.config['MONGODB_SETTINGS'] = {
        'db': 'dictionary',
        'host': 'mongodb://techlab_rt:example_pw@127.0.0.1:27017/dictionary?authSource=admin&authMechanism=SCRAM-SHA-256',
        'connect': True
    }
    configure_database(app)
    return app
