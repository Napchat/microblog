from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
	#: the DataRequired import is a validator, a function that
	#: can be attached to a field to perform validation on the
	#: data submitted by the user. The DataRequired validator
	#: simply checks that the field is not submitted empty.
	openid = StringField('openid', validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default=False)

class EditForm(FlaskForm):
	nickname = StringField('nickname', validators=[DataRequired()])
	about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])