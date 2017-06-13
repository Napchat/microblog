#!flask/bin/python3
import os
import unittest

from config import basedir
from app import app, db
from app.models import User

class TestCase(unittest.TestCase):
    #: setUp and tearDown methods run before and after each test respectively.
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

if __name__ == '__main__':
    unittest.main()