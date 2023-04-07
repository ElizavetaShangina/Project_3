import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Review(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'reviews'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    ending_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("endings.id"))
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now())
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    mark = sqlalchemy.Column(sqlalchemy.Integer)
    ending = orm.relationship('Ending')
    user = orm.relationship("User")