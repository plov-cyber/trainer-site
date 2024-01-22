# coding=utf-8
# Импорты необходимых библиотек, классов и функций
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddIdiomForm(FlaskForm):
    """Класс формы для добавления новой идиомы"""

    text = StringField('Текст идиомы', validators=[DataRequired('Введите текст идиомы')])
    meaning = StringField('Значение идиомы', validators=[DataRequired('Введите значение идиомы')])

    submit = SubmitField('Добавить')
