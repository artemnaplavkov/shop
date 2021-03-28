import flask
from flask import request, jsonify
from .db_session import SqlAlchemyBase

from flask_restful import reqparse, abort, Api, Resource
from . import db_session
from .orders import Order


order_parser = reqparse.RequestParser()
order_parser.add_argument('order_id', required=True, type=int)
order_parser.add_argument('user_id', required=True, type=int)
order_parser.add_argument('bought_at', required=True)


def abort_if_order_not_found(order_id):
    session = db_session.create_session()
    order = session.query(Order).get(order_id)
    if not order:
        abort(404, message=f"Order {order_id} not found")

order_field = ('order_id', 'user_id', 'bought_at')

class OrderResource(Resource):
    def get(self, order_id):
        abort_if_order_not_found(order_id)
        session = db_session.create_session()
        order = session.query(Order).get(order_id)
        return jsonify({'order': order.to_dict(
            only=order_field)})

    def delete(self, order_id):
        abort_if_order_not_found(order_id)
        session = db_session.create_session()
        order = session.query(Order).get(order_id)
        session.delete(order)
        session.commit()
        return jsonify({'success': 'OK'})


class OrderListResource(Resource):
    def get(self):
        session = db_session.create_session()
        order = session.query(Order).all()
        return jsonify({'order': [item.to_dict(
            only=order_field) for item in order]})

    def post(self):
        args = order_parser.parse_args()
        session = db_session.create_session()
        order = Order(
            order_id=args['order_id'],
            user_id=args['user_id'],
            bought_at=args['bought_at']
        )
        session.add(order)
        session.commit()
        return jsonify({'success': 'OK'})
