from flask import Flask, render_template, redirect, make_response, jsonify
from data import db_session
from data.tables.users import User
from data.tables.combos import Combo
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from forms.user import LoginForm, RegisterForm
from flask_restful import abort, Api
from flask_ngrok import run_with_ngrok
from data.tables.passings import Passing
from forms.ending import EndingForm
from data.tables.reviews import Review

app = Flask(__name__)
api = Api(app)
run_with_ngrok(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


from data.api import passing_api, login_api


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(passing_api.blueprint)
    app.register_blueprint(login_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
