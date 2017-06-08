# -*- coding: utf-8 -*-

#: for the cross-site request forgery prevention
WTF_CSRF_ENABLED = True

#: this is needed when CSRF is enabled, it is
#: used to create a cryptographic token that is
#: used to validate a form. Make sure to set the
#: secret key to something that is difficult to guess.
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}
]