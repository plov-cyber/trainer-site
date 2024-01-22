# coding=utf-8
# Импорты необходимых библиотек, классов и функций
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, SelectField
from wtforms.validators import ValidationError, InputRequired


class AtLeastOne(object):
    def __init__(self, message=None):
        if not message:
            message = 'At least one field should be provided'
        self.message = message

    def __call__(self, form, field):
        if not any((f.data != '') for f in field):
            raise ValidationError(self.message)


class AddQuestionForm(FlaskForm):
    """Класс формы для добавления вопроса в тест"""

    idiom = SelectField('Идиома', coerce=int)

    options = FieldList(StringField('Вариант ответа'),
                        validators=[AtLeastOne(message='Введите хотя бы один вариант ответа')],
                        min_entries=4)

    submit = SubmitField('Добавить')
