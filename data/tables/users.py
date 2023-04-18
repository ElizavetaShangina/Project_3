import sqlalchemy
from flask_login import UserMixin
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    """Пользователи"""
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    reviews = orm.relationship("Review", back_populates="user")
    combos = orm.relationship("Combo", back_populates="user")
    passings = orm.relationship("Passing", back_populates="user")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)