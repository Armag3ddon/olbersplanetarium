#
# E-mail sending
#

from flask import render_template, current_app
from flask_mail import Message
from flask_babel import _
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from app import mail
from config import Config
from threading import Thread

def generate_token(email, secret_key, salt):
    s = URLSafeTimedSerializer(secret_key)
    return s.dumps(email, salt=salt)

def verify_token(token, secret_key, salt, expiration):
    s = URLSafeTimedSerializer(secret_key)
    try:
        return True, s.loads(token, salt=salt, max_age=expiration)
    except SignatureExpired:
        return False, _('Fehler: der Sicherheitstoken ist nicht mehr gültig.')  # Token has expired
    except BadSignature:
        return False, _('Fehler: der Sicherheitstoken ist nicht gültig.')  # Invalid token

def send_email(to, subject, template, **kwargs):
    msg = Message(subject, recipients=[to], sender=Config.MAIL_DEFAULT_SENDER)
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    try:
        Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
    except Exception as e:
        return _(' Fehler beim Senden der E-Mail: {}').format(str(e))
    return _(' E-Mail wird versendet an {}.').format(to)

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)