# Импорты необходимых библиотек, классов и функций
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Question(SqlAlchemyBase, SerializerMixin):
    """Класс Вопроса"""
    __tablename__ = 'questions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    options = orm.relationship('Option', back_populates='question', cascade="all, delete")
    answer = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    idiom_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('idioms.id'))
    idiom = orm.relationship('Idiom', back_populates='questions')

    # TODO: delete questions when deleting test
    test_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('tests.id'), nullable=False)
    test = orm.relationship('Test', back_populates='questions')
