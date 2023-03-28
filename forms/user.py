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


def make_settings_form(default):
    class SettingsForm(FlaskForm):
        hardness = SelectField("Выбор сложности", choices=["Сложно", "Средне", "Легко"],
                               name="button",
                               default=default)
        submit = SubmitField("Применить", name="enter")
    return SettingsForm()
    # почему то именно у SelectField нельзя по нормальному установить дефолтное значение через
    # шаблоны, т. е. через параметр value, а через класс, унаследованный от FlaskForm, не получается
    # поменять значение под каждого user'а в БД, можно поставить дефолтное только всем
    # объектам класса сразу, а потому приходится делать через костыли
