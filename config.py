import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'c54ec5889e42b654e72263365d299a8f001bf2e91c0f0fdc244117ca14b6340a'
    # Flask-sqlalchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    # Flask-bootstrap
    BOOTSTRAP_SERVE_LOCAL = True # avoid GDPR troubles
    # Flask-babel
    LANGUAGES = ['de', 'en']
    # Uploading avatars / profile pictures
    UPLOAD_FOLDER = os.path.join(basedir, 'app/avatars')