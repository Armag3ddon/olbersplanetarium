#
# E-mail sending
#

from flask import render_template
from flask_mail import Message
from flask_babel import _
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from app import mail
from config import Config

def generate_token(email, secret_key, salt):
    s = URLSafeTimedSerializer(secret_key)
    return s.dumps(email, salt=salt)

def verify_token(token, secret_key, salt, expiration):
    s = URLSafeTimedSerializer(secret_key)
    try:
        return s.loads(token, salt=salt, max_age=expiration)
    except SignatureExpired:
        return _('Fehler: der Sicherheitstoken ist nicht mehr gültig.')  # Token has expired
    except BadSignature:
        return _('Fehler: der Sicherheitstoken ist nicht gültig.')  # Invalid token

def send_email(to, subject, template, **kwargs):
    msg = Message(subject, recipients=[to], sender=Config.MAIL_DEFAULT_SENDER)
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    try:
        mail.send(msg)
    except Exception as e:
        return _('Fehler beim Senden der E-Mail: {}').format(str(e))
    return _('E-Mail erfolgreich gesendet an {}.').format(to)