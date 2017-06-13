#!flask/bin/python3
import os
import unittest

from config import basedir
from app import app, db
from app.models import User

class TestCase(unittest.TestCase):
    # setUp and tearDown methods run before and after each test respectively.
    def setUp(self):
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

if __name__ == '__main__':
    unittest.main()