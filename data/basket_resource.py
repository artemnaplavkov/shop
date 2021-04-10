import flask
from flask import request, jsonify
from .db_session import SqlAlchemyBase

from flask_restful import reqparse, abort, Api, Resource
from . import db_session
from .basket import Basket


basket_parser = reqparse.RequestParser()
basket_parser.add_argument('quantity', required=True, type=int)
basket_parser.add_argument('price', required=True, type=float)
basket_parser.add_argument('user_id', required=True, type=int)
basket_parser.add_argument('product_id', required=True, type=int)



def abort_if_basket_not_found(user_id, product_id):
    session = db_session.create_session()
    basket = session.query(Basket).filter(
        Basket.user_id == user_id).filter(Basket.product_id == product_id)
    if basket.count() != 1:
        abort(
            404, message=f"Basket {user_id}, {product_id} not found")

basket_field = ('quantity', 'price', 'user_id', 'product_id')

class BasketResource(Resource):
    def get(self, user_id, product_id):
        abort_if_basket_not_found(user_id, product_id)
        session = db_session.create_session()
        basket = session.query(Basket).filter(
            Basket.user_id == user_id).filter(Basket.product_id == product_id).first()
        return jsonify({'basket': basket.to_dict(
            only=basket_field)})

    def delete(self, user_id, product_id):
        abort_if_basket_not_found(user_id, product_id)
        session = db_session.create_session()
        basket = session.query(Basket).filter(
            Basket.user_id == user_id).filter(Basket.product_id == product_id).first()
        session.delete(basket)
        session.commit()
        return jsonify({'success': 'OK'})


class BasketListResource(Resource):
    def get(self):
        session = db_session.create_session()
        basket = session.query(Basket).all()
        return jsonify({'basket': [item.to_dict(
            only=basket_field) for item in basket]})

    def post(self):
        args = basket_parser.parse_args()
        session = db_session.create_session()
        order = Basket(
            quantity=args['quantity'],
            price=args['price'],
            user_id=args['user_id'],
            product_id=args['product_id']
        )
        session.add(order)
        session.commit()
        return jsonify({'success': 'OK'})
