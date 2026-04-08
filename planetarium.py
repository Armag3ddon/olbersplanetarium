import sqlalchemy as sa
import sqlalchemy.orm as so
from app import create_app, db
from app.models import User, Right, CalendarEntry, Post

app = create_app()

# Populate the "flask shell" command with the database connection and database models
@app.shell_context_processor
def make_shell_context():
    return { 'sa': sa, 'so': so, 'db': db, 'User': User, 'Right': Right, 'CalendarEntry': CalendarEntry, 'Post': Post }

# How to create the first admin user in a new database:
# 1. Run "flask shell" in the terminal
# 2. In the shell, run the following commands:
# import pyotp
# user=User(username='USERNAME', email='EMAIL@DOMAIN.DE', token_2fa=pyotp.random_base32())
# db.session.add(user)
# db.session.commit()
# db.session.refresh(user)
# rights=Right(user_id=user.id, admin=True)
# db.session.add(rights)
# db.session.commit()
# from app.email.mail_utils import generate_token
# token=generate_token('EMAIL@DOMAIN.DE', 'SECRET_KEY', 'email-registration')
# print(token)
# exit()
# 3. Copy the printed token and open the following URL in the browser, replacing TOKEN with the copied token:
# https://applicationdomain/verify?token=TOKEN