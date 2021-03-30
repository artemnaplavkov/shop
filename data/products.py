import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class Product(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'products'

    product_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   primary_key=True, autoincrement=True)
    product_name = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    quantity = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
