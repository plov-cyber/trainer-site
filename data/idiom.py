# Импорты необходимых библиотек, классов и функций
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Idiom(SqlAlchemyBase, SerializerMixin):
    """Класс Идиомы"""
    __tablename__ = 'idioms'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    text = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    meaning = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    creator_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    creator = orm.relationship('User', back_populates='idioms')

    questions = orm.relationship('Question', back_populates='idiom')
