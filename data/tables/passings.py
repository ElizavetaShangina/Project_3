import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm
from datetime import datetime


class Passing(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'passings'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    ending_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("endings.id"))
    username = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.name"))
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.now())
    ending = orm.relationship('Ending')
    user = orm.relationship("User")