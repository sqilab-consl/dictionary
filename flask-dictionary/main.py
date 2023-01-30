from flask import render_template
from flask_mongoengine import MongoEngine
from apps import create_app
from apps.config import config_dict
from logging.config import dictConfig

dictConfig({
    'version': 1,   
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

# Create app
app = create_app(config_dict['Production'])

DEBUG=True
# serve default public home page
@app.route("/")
def hello_world():
    return render_template('public/index.html')

def main():
    app.run(debug=True,port=3200,host='0.0.0.0')

if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG))
if __name__=='__main__':
    main()