# coding=utf-8
# Импорты необходимых библиотек, классов и функций
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, SelectField
from wtforms.validators import ValidationError, InputRequired


class AnswerQuestionForm(FlaskForm):
    """Класс формы для ответа на вопрос"""

    idiom = StringField(label='Текст идиомы')
    options = SelectField(label="Варианты ответа")
