# -*- coding: utf-8 -*-
#!flask/bin/python3
import os

# for the cross-site request forgery prevention
WTF_CSRF_ENABLED = True

# this is needed when CSRF is enabled, it is
# used to create a cryptographic token that is
# used to validate a form. Make sure to set the
# secret key to something that is difficult to guess.
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
    {'name': 'OpenID', 'url': 'http://<username>.openid.org.cn'},
]

basedir = os.path.abspath(os.path.dirname(__file__))

# path of our database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

# the folder where we will store our migrate data files
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# mail server settings
MAIL_SERVER = 'www.163.com'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

# administrator list
ADMINS = ['wozhendeaiwoa@163.com']

# pagenation
POSTS_PER_PAGE = 3

# the name of the full text search database
WHOOSH_BASE = os.path.join(basedir, 'search.db')

MAX_SEARCH_RESULTS = 50