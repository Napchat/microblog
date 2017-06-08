# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
	#: fake user
	user = {'nickname': 'Miguel'}

	#: fake array of posts
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
def login():
	form = LoginForm()

	#: the validate_on_submit() method does all the form processing work.
	if form.validate_on_submit():
		#: The flash function is a quick way to show a message on the next page presented to the user. The 
		#: flash function is also extremely useful on production servers to provide feedback to the user 
		#: regarding an action.
		flash('Login requested for OpenID="%s", remember_me=%s' %
			  (form.openid.data, str(form.remember_me.data)))
		return redirect('/index')
	return render_template('login.html',
						   title='Sign In',
						   form=form,
						   providers=app.config['OPENID_PROVIDERS'])