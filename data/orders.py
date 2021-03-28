import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from .users import User
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class Order(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'orders'

    order_id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey(User.id), nullable=False)
    bought_at = sqlalchemy.Column(sqlalchemy.DateTime)
    user = orm.relation('User')
