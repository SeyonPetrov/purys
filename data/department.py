import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from data.users import User
from data import db_session


class Department(SqlAlchemyBase):
    __tablename__ = 'department'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           sqlalchemy.ForeignKey('users.'),
                           autoincrement=True, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    chief = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    members = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.BLOB)
    user = orm.relationship('User')
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
