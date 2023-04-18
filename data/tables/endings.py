import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash


class Ending(SqlAlchemyBase, SerializerMixin):
    """Концовки (прохождения != концовки)"""
    __tablename__ = 'endings'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    path_to_picture = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    reviews = orm.relationship("Review", back_populates="ending")
    passings = orm.relationship("Passing", back_populates="ending")