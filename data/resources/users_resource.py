from flask_restful import abort, Resource
from flask import jsonify
from data.resources.resources_parsers import users_settings_get_parser
from data.tables.users import User
from data import db_session


class UsersListResource(Resource):
    # пусть пока так будет делаться авторизация, может потом поменяю
    def post(self):
        args = users_settings_get_parser.parse_args()
        session = db_session.create_session()
        user = session.query(User).filter(User.name == args["name"]).first()
        if user and user.check_password(args["password"]):
            return jsonify({'settings': user.to_dict(only=("hardness",))})
        abort(400, message="Password or name are wrong")
    # других методов пока не надо
