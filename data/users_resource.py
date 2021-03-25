import flask
from flask import request, jsonify
from flask_login import UserMixin
from .db_session import SqlAlchemyBase

from flask_restful import reqparse, abort, Api, Resource
from . import db_session
from .users import User


user_parser = reqparse.RequestParser()
user_parser.add_argument('id', required=True, type=int)
user_parser.add_argument('login', required=True)
user_parser.add_argument('password', required=True)


def abort_if_user_not_found(id):
    session = db_session.create_session()
    user = session.query(User).get(id)
    if not user:
        abort(404, message=f"User {id} not found")

user_field = ('id', 'login', 'password')

class UserResource(Resource):
    def get(self, id):
        abort_if_user_not_found(id)
        session = db_session.create_session()
        user = session.query(User).get(id)
        return jsonify({'user': user.to_dict(
            only=user_field)})

    def delete(self, id):
        abort_if_user_not_found(id)
        session = db_session.create_session()
        user = session.query(User).get(id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()
        return jsonify({'user': [item.to_dict(
            only=user_field) for item in user]})

    def post(self):
        args = user_parser.parse_args()
        session = db_session.create_session()
        user = User(
            id=args['id'],
            login=args['login'],
            password=args['password']
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
