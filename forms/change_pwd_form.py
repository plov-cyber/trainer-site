# coding=utf-8
# Импорты необходимых библиотек, классов и функций
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired


class ChangePasswordForm(FlaskForm):
    """Класс для смены пароля в аккаунте"""
    old_password = PasswordField('Старый пароль', validators=[DataRequired(message='Введите старый пароль')])
    new_password = PasswordField('Пароль',
                                 validators=[DataRequired(message='Введите новый пароль')])
    submit = SubmitField('Сохранить')
