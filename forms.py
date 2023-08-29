from flask import url_for
from flask_wtf import FlaskForm, RecaptchaField
from markupsafe import Markup
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=10, message='Name is too short')])
    email = EmailField('Email',
                       validators=[DataRequired(), Length(min=2, max=50, message='Email is too short'), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=2, max=20, message='Password is too short')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),

                                                                     EqualTo('password',
                                                                             message='Passwords must match')])
    accept_tos = BooleanField(Markup('I accept the <a href="">TOS</a> -'), validators=[DataRequired()], default=False)
    recaptcha = RecaptchaField()  # Verify you're human: {{ form.recaptcha }}
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.accept_tos.label.text = Markup("I accept the <a href='{}'>TOS</a>".format(url_for('home')))

    # def validate(self):
    #     initial_validation = super(RegistrationForm, self).validate()
    #     if not initial_validation:
    #         return False
    # #     user = User.query.filter_by(username=self.username.data).first()
    #     if user:
    #         self.username.errors.append("Username already registered")
    #         return False
    #     user = User.query.filter_by(email=self.email.data).first()
    #     if user:
    #         self.email.errors.append("Email already registered")
    #         return False
    #     return True


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    recaptcha = RecaptchaField()
    submit = SubmitField('Log In')

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    # def validate(self):
    #     initial_validation = super(LoginForm, self).validate()
    #     if not initial_validation:
    #         return False
    #     user = User.query.filter_by(email=self.email.data).first()
    #     if not user:
    #         self.email.errors.append('Unknown email')
    #         return False
    #     if not user.verify_password(self.password.data):
    #         self.password.errors.append('Invalid password')
    #         return False
    #     return True
