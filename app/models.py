'''
app.models
~~~~~~~~~~

It defines our models related to tables in database.
'''

from hashlib import md5
import sys
import re

import flask_whooshalchemy as whooshalchemy

from app import db, app

followers = db.Table('followers', 
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    '''The User model'''
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)

    # :arg: ``User`` on both sides mean that this is a self-referential
    # relationship.
    # :arg: ``secondary`` indicates the association table that is used
    # for this relationship.
    # :arg: ``primaryjoin`` indicates the condition that links the left
    # side entity(the follower user) with the association table. Note that
    # because the :table:`followers` is not a model there is a slightly
    # odd syntax required to get to the field name.
    # :arg: ``secondaryjoin`` indicates the condition that links the
    # right side entity(the followed user) with the association table.
    # :arg: ``backref`` defines how this relationship will be accessed
    # from the right side entity.``lazy`` indicates the execution mode 
    # for this query. A mode of ``dynamic`` sets up the query to not run 
    # until specifically requested. This is userful for performance reasons, 
    # and also because we will be able to take this query and modify it before 
    # it executes. More about this later.
    # :arg: ``lazy`` is similiar to the parameter of the same name in the 
    # ``backref``, but this one applies to the regular query instead of the 
    # back reference.
    # u1关注u2, 那么u1就有followed属性(followers表中的follower_id设置为u1的id, 
    # followed_id设置为u2的id). 
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id==id),
                               secondaryjoin=(followers.c.followed_id==id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

    @property
    def is_authenticated(self):
        '''pass'''
        return True

    @property
    def is_active(self):
        '''pass'''
        return True

    @property
    def is_annoymous(self):
        '''pass'''
        return False

    def get_id(self):
        '''pass'''
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def avatar(self, size):
        '''This method returns the URL of the user's avatar image'''
        return 'https://gravatar.com/avatar/%s?d=mm&s=%d' % \
               (md5(self.email.encode('utf-8')).hexdigest(), size)

    def __repr__(self):
        '''This method tells Python how to print objects of
        this class.
        '''
        return '<User %r>' % (self.nickname)

    # staticmethod don't work on instances.
    @staticmethod
    def make_unique_nickname(nickname):
        '''pass'''
        if User.query.filter_by(nickname=nickname).first() is None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname=new_nickname).first() is None:
                break
            version += 1
        return new_nickname

    def follow(self, user):
        '''Follows a user.'''
        if not self.is_following(user):
            self.followed.append(user)
            return self
    
    def unfollow(self, user):
        '''Unfollows a user.'''
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        '''Check if you followed the user.'''
        return self.followed.filter(followers.c.followed_id==user.id).count() > 0

    def followed_posts(self):
        '''Return a query object including posts of the users that you have followed.
        It is always a good idea to return query object instead of results, because
        that gives the caller the choice of adding more clauses to the query before
        it is execeted.
        '''
        return Post.query.join(followers, (followers.c.followed_id==Post.user_id)). \
                               filter(followers.c.follower_id==self.id).order_by(Post.timestamp.desc())
    
    @staticmethod
    def make_valid_nickname(nickname):
        return re.sub('[^a-zA-Z0-0_\.]', '', nickname)

class Post(db.Model):
    '''The Post model'''

    # It is an array with all the database fields that will be in the searchable
    # index.
    __searchable__ = ['body']

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    language = db.Column(db.String(5))

    def __repr__(self):
        '''pass'''
        return '<Post %r>' % (self.body)

# To initialize the full text for models.
whooshalchemy.whoosh_index(app, Post)
