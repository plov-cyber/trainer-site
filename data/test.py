# Импорты необходимых библиотек, классов и функций
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Test(SqlAlchemyBase, SerializerMixin):
    """Класс Теста"""
    __tablename__ = 'tests'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    questions = orm.relationship('Question', back_populates='test')

    creator_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False)
    creator = orm.relationship('User', back_populates='tests_created')

    pupils = orm.relationship('User', secondary='test_to_pupil', backref='tests_available')
