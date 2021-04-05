import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from .users import User
from .products import Product
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class Basket(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'basket'

    quantity = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey(User.id), nullable=False, primary_key=True)
    product_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey(Product.product_id), nullable=False, primary_key=True)
    user = orm.relation('User')
    product = orm.relation('Product')
