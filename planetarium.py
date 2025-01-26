import sqlalchemy as sa
import sqlalchemy.orm as so
from app import create_app, db
from app.models import User, Right, CalendarEntry

app = create_app()

# Populate the "flask shell" command with the database connection and database models
@app.shell_context_processor
def make_shell_context():
    return { 'sa': sa, 'so': so, 'db': db, 'User': User, 'Right': Right, 'CalendarEntry': CalendarEntry }