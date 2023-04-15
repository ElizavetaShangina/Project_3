from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, \
    BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()], name="password")
    remember = BooleanField("Запомнить меня", name="checkbox")
    submit = SubmitField('Войти', name="enter")


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()], name="password")
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()], name="password")
    submit = SubmitField('Зарегистрироваться', name="enter")
