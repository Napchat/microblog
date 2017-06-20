# -*- coding: utf-8 -*-
#!flask/bin/python3

'''
Microblog here!
~~~~~~~~~~~~~~~

Initialization of our app, database, loginmanager, openid, mail.....

microblog is used for me learning flask, it has rich features:
1. User management, including managing logins, sessions, user roles, 
   profiles and user avatars.
2. Database management, including migration handling.
3. Web form support, including field validation.
4. Pagination of long lists of items.
5. Full text search.
6. Email notifications to users.
7. HTML templates.
8. Support for multiple languages.
9. Caching and other performance optimizations.
10. Debugging techniques for development and production servers.
11. Installation on a production server.

Hope for enjoying using this little blog.
'''

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_openid import OpenID
from flask_mail import Mail
from flask_babel import Babel, lazy_gettext

from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
from .momentjs import momentjs

app = Flask(__name__)
app.config.from_object('config')
app.config['DEBUG'] = True
app.config['flask_profiler'] = {
    'enabled': app.config['DEBUG'],
    'storage': {
        'engine': 'sqlite'
    },
    'basicAuth': {
        'enabled': True,
        'username': 'napchat',
        'password': '2291277'
    },
    'ignore': [
        '/static/*'
        'flask/*'
    ]
}

# this tells jinja2 to expose our class as a global variable to all templates.
app.jinja_env.globals['momentjs'] = momentjs

# initialize database
db = SQLAlchemy(app)

# initialize mail server
mail = Mail(app)

# initialize babel
babel = Babel(app)

lm = LoginManager()
lm.init_app(app)

# tell lm the view function name
lm.login_view = 'login'

# if we call gettext() outside of a request it will just give us the default
# text, which will be the English version. For cases like this, we have lazy_gettext()
# which seach for a translation until the string is actually used.
lm.login_message = lazy_gettext('Please log in to access this page.')

oid = OpenID(app, os.path.join(basedir, 'tmp'))

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1*1024*1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s \
                                                [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('Microblog start app.debug = %s' % app.debug)

from app import views, models