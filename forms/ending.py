from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, \
    BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired


class EndingForm(FlaskForm):
    comment = TextAreaField('Ваш комментарий', validators=[DataRequired()])
    submit = SubmitField('Отправить', name="enter")