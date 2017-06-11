# -*- coding: utf-8 -*-
#!flask/bin/python3
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm
from .models import User

@app.before_request
def before_request():
	g.user = current_user

@app.route('/')
@app.route('/index')
@login_required
def index():
	user = g.user

	posts = [
		{
			'author': {'nickname': 'John'},
			'body': 'Beautiful day in Portland!'
		},
		{
			'author': {'nickname': 'Susan'},
			'body': 'The Avengers movie was so cool!'
		}
	]

	return render_template('index.html',
						   title='Home',
						   user=user,
						   posts=posts)

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
	'''@oid.loginhandler decorator tells Flask_OpenID that
	this is our login view function.
	'''

	#: flask.g object stores and shares data through the life of a appcontext.
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()

	#: the validate_on_submit() method does all the form processing work.
	if form.validate_on_submit():
		#: once data is stored in the session object, it will be available
		#: during that request and any future requests made by the same client.
		#: data remains in the session until explicitly removed. 
		#: flask keeps a different session container for each client of our app.
		session['remember_me'] = form.remember_me.data

		#: the oid.try_login() method triggers the user authentication through
		#: Flask-OpenID. Two arguments, one is the openid given by the user in the 
		#: web form and the other is a list of data items that we want from the
		#: OpenID provider.
		return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
	return render_template('login.html',
						   title='Sign In',
						   form=form,
						   providers=app.config['OPENID_PROVIDERS'])

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@oid.after_login
def after_login(resp):
	'''if authentication is successful, this method ia called.'''
	if resp.email is None or resp.email == '':
		flash('Invalid login. Please try again.')
		return redirect(url_for('login'))

	user = User.query.filter_by(email=resp.email).first()
	if user is None:
		nickname = resp.nickname
		if nickname is None or nickname == '':
			nickname = resp.email.split('@')[0]
		user = User(nickname=nickname, email=resp.email)
		db.session.add(user)
		db.session.commit()
	remember_me = False
	if 'remember_me' in session:
		remember_me = session['remember_me']
		session.pop('remember_me', None)
	login_user(user, remember=remember_me)
	return redirect(request.args.get('next') or url_for('index'))
