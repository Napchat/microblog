from flask_mail import Message
from flask import render_template

from config import ADMINS
from app import mail

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, rencipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

def follower_notification(followed, follower):
    send_email('[microblog] %s is now following you!' % follower.nickname,
               ADMINS[0],
               [followed.email],
               render_template('follower_email.txt',
                               user=followed, followed=follower),
               render_template('follower_email.html',
                                user=followed, follower=follower))