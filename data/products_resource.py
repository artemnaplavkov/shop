import flask
from flask import request, jsonify
from .db_session import SqlAlchemyBase

from flask_restful import reqparse, abort, Api, Resource
from . import db_session
from .products import Product


product_parser = reqparse.RequestParser()
product_parser.add_argument('product_id', required=True, type=int)
product_parser.add_argument('product_name', required=True)
product_parser.add_argument('price', required=True, type=float)
product_parser.add_argument('quantity', required=True, type=int)


def abort_if_product_not_found(product_id):
    session = db_session.create_session()
    product = session.query(Product).get(product_id)
    if not product:
        abort(404, message=f"Product {product_id} not found")

product_field = ('product_id', 'product_name', 'price', 'quantity')

class ProductResource(Resource):
    def get(self, product_id):
        abort_if_product_not_found(product_id)
        session = db_session.create_session()
        product = session.query(Product).get(product_id)
        return jsonify({'product': product.to_dict(
            only=product_field)})

    def delete(self, product_id):
        abort_if_product_not_found(product_id)
        session = db_session.create_session()
        product = session.query(Product).get(product_id)
        session.delete(product)
        session.commit()
        return jsonify({'success': 'OK'})


class ProductListResource(Resource):
    def get(self):
        session = db_session.create_session()
        product = session.query(Product).all()
        return jsonify({'product': [item.to_dict(
            only=product_field) for item in product]})

    def post(self):
        args = product_parser.parse_args()
        session = db_session.create_session()
        product = Product(
            product_id=args['product_id'],
            product_name=args['product_name'],
            price=args['price'],
            quantity=args['quantity']
        )
        session.add(product)
        session.commit()
        return jsonify({'success': 'OK'})
