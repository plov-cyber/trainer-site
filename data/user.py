# Импорты необходимых библиотек, классов и функций
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase

# Промежуточная таблица связи учеников и тестов
test_to_pupil = sqlalchemy.Table('test_to_pupil', SqlAlchemyBase.metadata,
                                 sqlalchemy.Column('pupil_id', sqlalchemy.Integer,
                                                   sqlalchemy.ForeignKey('users.id')),
                                 sqlalchemy.Column('test_id', sqlalchemy.Integer,
                                                   sqlalchemy.ForeignKey('tests.id')))


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    """Класс Пользователя"""
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, index=True)
    login = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    is_teacher = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    tests_created = orm.relationship('Test', back_populates='creator', cascade='all, delete')
    idioms = orm.relationship('Idiom', back_populates='creator', cascade='all, delete')

    def set_password(self, password):
        """Функция установки пароля"""
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        """Функция проверки пароля"""
        return check_password_hash(self.hashed_password, password)
