import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    APP_NAME = os.environ.get('APP_NAME') or 'Olbers Planetarium'
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
    # Flask-mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') == 'True'
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') == 'True'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEBUG = os.environ.get('MAIL_DEBUG') == 'True'
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@nothig.com'
    # Debug Mode
    DEBUG = os.environ.get('DEBUG') is not None