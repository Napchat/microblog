'''
app.forms
~~~~~~~~~

Forms we need to use when posting datas in our website.

flask_wtf.Form is still useable, but FlaskForm is suggested.
'''

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    # the DataRequired import is a validator, a function that
    # can be attached to a field to perform validation on the
    # data submitted by the user. The DataRequired validator
    # simply checks that the field is not submitted empty.
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class EditForm(FlaskForm):
    nickname = StringField('nickname', validators=[DataRequired()])
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

    def __init__(self, original_nickname, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname=self.nickname.data).first()
        if user != None:
            self.nickname.errors.append('This nickname is already in use. \
                                        Please choose another one.')
            return False
        return True

class PostForm(FlaskForm):
    post = TextAreaField('post', validators=[DataRequired()])

class SearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])