# -*- coding: utf-8 -*-
#!flask/bin/python3

'''
app.views
~~~~~~~~~

view functions associated with every URLs of our web App

And I am going to modify it with blueprint feature of Flask.
'''

from datetime import datetime

from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from flask_babel import gettext
from guess_language import guessLanguage
import flask_profiler
from flask_sqlalchemy import get_debug_queries

from app import app, db, lm, oid, babel
from .forms import LoginForm, EditForm, PostForm, SearchForm
from .models import User, Post
from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS, LANGUAGES, DATABSE_QUERY_TIMEOUT
from .emails import follower_notification

# the function that is marked with the ``localeselector`` decorator will be
# called before each request to give us a chance to choose the language to use
# when producing its response.
@babel.localeselector
def get_locale():
    '''Read the Accept-Langusges header sent by the browser in the HTTP request
    and find the best matching langusge that we support.
    '''
    #return 'es'
    return request.accept_languages.best_match(LANGUAGES.keys())

@app.before_request
def before_request():
    '''Run before each request.'''
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = get_locale()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
@login_required
def index(page=1):
    form = PostForm()
    if form.validate_on_submit():
        language = guessLanguage(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post(
            body=form.post.data,
            timestamp=datetime.utcnow(),
            author=g.user,
            language=language
        )
        db.session.add(post)
        db.session.commit()
        flash(gettext('Your post is now live!'))

        # why redirect?  Consider what if users refresh their browser after
        # they write a post and submit it? Browsers resend the last issued 
        # request as a result of a refresh command. without the redirect, the
        # last request is the POST request that submit the form, so the refresh
        # will resubmit the form and causing a second Post record that is identical
        # to the first to be written to the database. By having the redirect, we
        # force the browser to issue another request.(This is a simple GET request
        # so a refresh will now repeat the GET request)
        return redirect(url_for('index'))

    # arguments: (page number, the number of items per page, an error flag)
    posts = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False)

    return render_template('index.html', title='Home',
                           form=form, posts=posts)

# @oid.loginhandler decorator tells Flask_OpenID that
# this is our login view function.
@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    ''''''

    # flask.g object stores and shares data through the life of a appcontext.
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    # the validate_on_submit() method does all the form processing work.
    if form.validate_on_submit():
        # once data is stored in the session object, it will be available
        # during that request and any future requests made by the same client.
        # data remains in the session until explicitly removed. 
        # flask keeps a different session container for each client of our app.
        session['remember_me'] = form.remember_me.data

        # the oid.try_login() method triggers the user authentication through
        # Flask-OpenID. Two arguments, one is the openid given by the user in the 
        # web form and the other is a list of data items that we want from the
        # OpenID provider.
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

@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname, page=1):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash(gettext('User %(nickname)s not found.', nickname=nickname))
        return redirect(url_for('index'))
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('user.html',
                           user=user,
                           posts=posts)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@oid.after_login
def after_login(resp):
    '''if authentication is successful, this method ia called.'''
    if resp.email is None or resp.email == '':
        flash(gettext('Invalid login. Please try again.'))
        return redirect(url_for('login'))

    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == '':
            nickname = resp.email.split('@')[0]
        nickname = User.make_valid_nickname(nickname)
        nickname = User.make_unique_nickname(nickname)
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
        db.session.add(user.follow(user))
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash(gettext('Your changes have beem saved.'))
        return redirect(url_for('user', nickname=g.user.nickname))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash(gettext('User %(nickname)s is not found.', nickname=nickname))
        return redirect(url_for('index'))
    if user == g.user:
        flash(gettext("You can't follow yourself!"))
        return redirect(url_for('user', nickname=nickname))
    u = g.user.follow(user)
    if u is None:
        flash(gettext('Cannot follow %(nickname)s.', nickname=nickname))
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash(gettext('You are now following %(nickname)s', nickname=nickname))
    follower_notification(user, g.user)
    return redirect(url_for('user', nickname=nickname))

@app.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash(gettext('User %(nickname)s if not found.', nickname=nickname))
        return redirect(url_for('index'))
    if user == g.user:
        flash(gettext("You can't unfollow yourself!"))
        return redirect(url_for('user', nickname=nickname))
    u = g.user.unfollow(user)
    if u is None:
        flash(gettext('Cannot unfollow %(nickname)s', nickname=nickname))
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash(gettext('You have stopped following %(nickname)s.', nickname=nickname))
    return redirect(url_for('user', nickname=nickname))

@app.route('/search', methods=['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query=g.search_form.search.data))

@app.route('/search_results/<query>')
@login_required
def search_results(query):
    results = Post.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    return render_template('search_results.html',
                           query=query,
                           results=results)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    post = Post.query.get(id)
    if post is None:
        flash('Post is not found')
        return redirect(url_for('index'))
    if post.author.id != g.user.id:
        flash('You cannot delete this post.')
        return redirect(url_for('index'))
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.')
    return redirect(url_for('index'))

@app.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= DATABSE_QUERY_TIMEOUT:
            app.logger.warning('SLOW QUERY: %s\nParameters: %s\Duration: %fs\nContext: %s\n' % \
                (query.statement, query.parameters, query.duration, query.context))
    return response

flask_profiler.init_app(app)