'''
app.emails
~~~~~~~~~~~~~~~~

Defining all the email functions here.
'''

from flask_mail import Message
from flask import render_template

from config import ADMINS
from app import mail, app
from .decorators import async_dec

@async_dec
def send_async_email(app, msg):
    '''Send mail asynchronously.'''
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    '''Set email content and send it asynchronously'''
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(app, msg)

def follower_notification(followed, follower):
    '''Emailing to users for being followed.'''
    send_email('[microblog] %s is now following you!' % follower.nickname,
                              ADMINS[0],
                              [followed.email],
                              render_template('follower_email.txt',
                                              user=followed, follower=follower),
                              render_template('follower_email.html',
                                              user=followed, follower=follower))