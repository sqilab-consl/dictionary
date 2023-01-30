
from flask_mongoengine import MongoEngine

from .models import Users

db=MongoEngine()

def initialize_database(app):
    app.logger.info('INIT database 2')
    db.init_app(app)