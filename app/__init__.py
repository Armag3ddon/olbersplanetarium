from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap

# Load modules
bootstrap = Bootstrap()

# Create the app, called in 
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initiate modules
    bootstrap.init_app(app)

    # Load error handling blueprint
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    return app