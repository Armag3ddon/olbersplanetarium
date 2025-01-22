from flask import Flask, request, current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5
from flask_babel import Babel
from flask_login import LoginManager

# For babel: get preferred language
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])

# Load modules
bootstrap = Bootstrap5()
db = SQLAlchemy()
migrate = Migrate()
babel = Babel()
login = LoginManager()

# Create the app, called in 
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initiate modules
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    babel.init_app(app, default_locale='de', locale_selector=get_locale)
    login.init_app(app)
    login.login_view = 'auth.login'

    # Load error handling blueprint
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    # Load authentication process (logging in)
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    # Load main application (logged in)
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # Inject babel's selected locale to the context processor
    # Available simply as 'lang' in templates (see base.html)
    @app.context_processor
    def utility_processor():
        return dict(lang=get_locale())

    return app

from app import models