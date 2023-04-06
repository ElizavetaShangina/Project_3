import sqlalchemy
from flask_login import UserMixin
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash


class Combo(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'combos'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    combo = sqlalchemy.Column(sqlalchemy.String,
                              unique=True, nullable=False)
    username = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.name"))
    user = orm.relationship("User")
