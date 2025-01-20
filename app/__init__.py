from flask import Flask
from flask_bootstrap import Bootstrap

# Load modules
bootstrap = Bootstrap()

# Create the app, called in 
def create_app():
    app = Flask(__name__)

    # Initiate modules
    bootstrap.init_app(app)

    # Load error handling blueprint
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    return app