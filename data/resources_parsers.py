from flask_restful import reqparse

users_settings_get_parser = reqparse.RequestParser()
users_settings_get_parser.add_argument("name", required=True, type=str)
users_settings_get_parser.add_argument("password", required=True, type=str)