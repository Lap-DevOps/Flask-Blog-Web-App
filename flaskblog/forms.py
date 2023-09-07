from flask import url_for
from flask_wtf import FlaskForm, RecaptchaField
from markupsafe import Markup
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=10, message='Name is too short')])
    email = EmailField('Email',
                       validators=[DataRequired(), Length(min=2, max=50, message='Email is too short'), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=2, max=20, message='Password is too short'),
                                         EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    accept_tos = BooleanField(Markup('I accept the <a href="">TOS</a> -'), validators=[DataRequired()], default=False)
    recaptcha = RecaptchaField()
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.accept_tos.label.text = Markup("I accept the <a href='{}'>TOS</a>".format(url_for('home')))

    def validate_username(self, username):
        excluded_chars = " *?!'^+%&/()=}][{$#"
        for char in self.username.data:
            if char in excluded_chars:
                raise ValidationError(
                    f"Character {char} is not allowed in username.")

    # def validate_email(self, field):
    #     if User.query.filter_by(email=field.data).first():
    #         raise ValidationError(
    #               'This email is already registered. Please use a different one.')
    #
    # def validate_username(self, field):
    #     if User.query.filter_by(username=field.data).first():
    #         raise ValidationError('This username is already taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = EmailField('Email',
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