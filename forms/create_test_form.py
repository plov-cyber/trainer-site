# coding=utf-8
# Импорты необходимых библиотек, классов и функций
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CreateTestForm(FlaskForm):
    """Класс формы для создания теста"""

    name = StringField('Название теста', validators=[DataRequired('Введите название теста')])

    submit = SubmitField('Далее')
