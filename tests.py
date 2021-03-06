#!flask/bin/python3
import os
import unittest
from datetime import datetime, timedelta

from coverage import coverage

from config import basedir
from app import app, db
from app.models import User, Post

cov = coverage(branch=True, omit=['flask/*', 'tests.py'])
cov.start()

class TestCase(unittest.TestCase):
    # setUp and tearDown methods run before and after each test respectively.
    def setUp(self):
        # during setup the ``TESTING`` config flag is activated. What it does is disable the error 
        # catching during request handling so that you get better error reports when performing 
        # test requests against the application.
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                                os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_avatar(self):
        u = User(nickname='Napchat', email='wozhendeaiwoa@gmail.com')
        avatar = u.avatar(128)
        expected = 'https://gravatar.com/avatar/662ab453eaf5d875abdab3ec6db2ad5d?d=mm&s=128'
        assert avatar[0:len(expected)] == expected
    
    def test_make_unique_nickname(self):
        u = User(nickname='Napchat', email='wozhendeaiwoa@gmail.com')
        db.session.add(u)
        db.session.commit()
        nickname = User.make_unique_nickname('Napchat')
        assert nickname != 'Napchat'
        u = User(nickname=nickname, email='wozhendeaiwoa@163.com')
        db.session.add(u)
        db.session.commit()
        nickname2 = User.make_unique_nickname('Napchat')
        assert nickname2 != 'Napchat'
        assert nickname2 != nickname

    def test_follow(self):
        u1 = User(nickname='Napchat', email='wozhendeaiwoa@gmail.com')
        u2 = User(nickname='NoNick', email='shangnan543@163.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        assert u1.unfollow(u2) is None
        u = u1.follow(u2)
        db.session.add(u)
        db.session.commit()
        assert u1.follow(u2) is None
        assert u1.is_following(u2)
        assert u1.followed.count() == 1
        assert u1.followed.first().nickname == 'NoNick'
        assert u2.followers.count() == 1
        assert u2.followers.first().nickname == 'Napchat'
        u = u1.unfollow(u2)
        assert u is not None
        db.session.add(u)
        db.session.commit()
        assert not u1.is_following(u2)
        assert u1.followed.count() == 0
        assert u2.followers.count() == 0

    def test_follow_posts(self):
        u1 = User(nickname='john', email='john@example.com')
        u2 = User(nickname='susan', email='susan@example.com')
        u3 = User(nickname='mary', email='mary@example.com')
        u4 = User(nickname='david', email='david@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(u4)

        utcnow = datetime.utcnow()
        p1 = Post(body='post from john', author=u1, timestamp=utcnow+timedelta(seconds=1))
        p2 = Post(body='post from susan', author=u2, timestamp=utcnow+timedelta(seconds=2))
        p3 = Post(body='post from mary', author=u3, timestamp=utcnow+timedelta(seconds=3))
        p4 = Post(body='post from david', author=u4, timestamp=utcnow+timedelta(seconds=4))
        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)
        db.session.add(p4)
        db.session.commit()

        u1.follow(u1)
        u1.follow(u2)
        u1.follow(u4)
        u2.follow(u2)
        u2.follow(u3)
        u3.follow(u3)
        u3.follow(u4)
        u4.follow(u4)
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(u4)
        db.session.commit()

        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        assert len(f1) == 3
        assert len(f2) == 2
        assert len(f3) == 2
        assert len(f4) == 1
        assert f1 == [p4, p2, p1]
        assert f2 == [p3, p2]
        assert f3 == [p4, p3]
        assert f4 == [p4]

    def test_delete_post(self):
        # create a user and a post
        u = User(nickname='john', email='john@example.com')
        p = Post(body='test post', author=u, timestamp=datetime.utcnow())
        db.session.add(u)
        db.session.add(p)
        db.session.commit()
        # query the post and dextroy the session
        p = Post.query.get(1)
        db.session.remove()
        # delete the post using a new session
        db.session = db.create_scoped_session()
        db.session.delete(p)
        db.session.commit()

if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
    cov.stop()
    cov.save()
    print('\n\nCoverage Report:\n')
    cov.report()
    print("HTML version: " + os.path.join(basedir, 'tmp/coverage/index.html'))
    cov.html_report(directory='tmp/coverage')
    cov.erase()