from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, \
    BooleanField, IntegerField, SelectField, DecimalRangeField
from wtforms.validators import DataRequired, NumberRange


class EndingForm(FlaskForm):
    """Форма для прохождения"""
    comment = TextAreaField('Ваш комментарий', validators=[DataRequired()])
    slider = DecimalRangeField("Оценка", validators=[NumberRange(min=0, max=10)],
                               render_kw={"step": "1"})
    submit = SubmitField('Отправить', name="enter")