import flask
from flask import request, jsonify
from .db_session import SqlAlchemyBase

from flask_restful import reqparse, abort, Api, Resource
from . import db_session
from .order_details import OrderDetails


order_details_parser = reqparse.RequestParser()
order_details_parser.add_argument('quantity', required=True, type=int)
order_details_parser.add_argument('price', required=True, type=float)
order_details_parser.add_argument('order_id', required=True, type=int)
order_details_parser.add_argument('product_id', required=True, type=int)



def abort_if_order_details_not_found(order_id, product_id):
    session = db_session.create_session()
    order_details = session.query(OrderDetails).filter(
        OrderDetails.order_id == order_id).filter(OrderDetails.product_id == product_id)
    if order_details.count() != 1:
        abort(
            404, message=f"OrderDetails {order_id}, {product_id} not found")

order_details_field = ('quantity', 'price', 'order_id', 'product_id')

class OrderDetailsResource(Resource):
    def get(self, order_id, product_id):
        abort_if_order_details_not_found(order_id, product_id)
        session = db_session.create_session()
        order_details = session.query(OrderDetails).filter(
            OrderDetails.order_id == order_id).filter(OrderDetails.product_id == product_id).first()
        return jsonify({'order_details': order_details.to_dict(
            only=order_details_field)})

    def delete(self, order_id, product_id):
        abort_if_order_details_not_found(order_id, product_id)
        session = db_session.create_session()
        order_details = session.query(OrderDetails).filter(
            OrderDetails.order_id == order_id).filter(OrderDetails.product_id == product_id).first()
        session.delete(order_details)
        session.commit()
        return jsonify({'success': 'OK'})


class OrderDetailsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        order_details = session.query(OrderDetails).all()
        return jsonify({'order_details': [item.to_dict(
            only=order_details_field) for item in order_details]})

    def post(self):
        args = order_details_parser.parse_args()
        session = db_session.create_session()
        order = OrderDetails(
            quantity=args['quantity'],
            price=args['price'],
            order_id=args['order_id'],
            product_id=args['product_id']
        )
        session.add(order)
        session.commit()
        return jsonify({'success': 'OK'})
