from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
	#: the DataRequired import is a validator, a function that
	#: can be attached to a field to perform validation on the
	#: data submitted by the user. The DataRequired validator
	#: simply checks that the field is not submitted empty.
	openid = StringField('openid', validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default=False)