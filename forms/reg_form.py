# coding=utf-8
# Импорты необходимых библиотек, классов и функций
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, EqualTo


class RegisterForm(FlaskForm):
    """Класс формы для регистрации пользователя"""
    login = StringField('Логин', validators=[DataRequired(message='Введите логин')])
    password = PasswordField('Пароль', validators=[DataRequired(message='Введите пароль')])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired(message='Введите пароль заново'),
                                                                   EqualTo('password', message='Пароли различаются')])

    surname = StringField('Фамилия', validators=[DataRequired(message='Введите фамилию')])
    name = StringField('Имя', validators=[DataRequired(message='Введите имя')])

    is_teacher = BooleanField('Я Учитель')

    submit = SubmitField('Зарегистрироваться')
