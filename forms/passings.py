from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, \
    BooleanField, IntegerField, SelectField, DecimalRangeField
from wtforms.validators import DataRequired, NumberRange


class SortForm(FlaskForm):
    type = SelectField('Сортировать по', validators=[DataRequired()],
                       choices=["id", "дате", "названию"], default="дате")
    reverse = BooleanField("Перевернуть", default=True)
    submit = SubmitField('Обновить', name="enter")