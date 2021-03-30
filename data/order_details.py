import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from .orders import Order
from .products import Product
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm


class OrderDetails(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'order_details'

    quantity = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    order_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey(Order.order_id), nullable=False, primary_key=True)
    product_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey(Product.product_id), nullable=False, primary_key=True)
    order = orm.relation('Order')
    product = orm.relation('Product')
