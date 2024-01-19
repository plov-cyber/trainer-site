# Импорты необходимых библиотек, классов и функций
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Option(SqlAlchemyBase, SerializerMixin):
    """Класс Варианта Ответа"""
    __tablename__ = 'options'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    text = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    question_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('questions.id'), nullable=False)
    question = orm.relationship('Question', back_populates='options')
