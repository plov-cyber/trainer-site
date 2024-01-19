# coding=utf-8
# Импорты необходимых библиотек, классов и функций
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """Класс формы для входа в аккаунт"""
    login = StringField('Логин', validators=[DataRequired(message='Введите логин')])
    password = PasswordField('Пароль', validators=[DataRequired(message='Введите пароль')])

    remember_me = BooleanField('Запомнить это устройство')

    submit = SubmitField('Войти')
