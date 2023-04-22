from flask import Flask, render_template, redirect
from flask_login import LoginManager
from flask_restful import Api
from data import db_session
from data.tables.users import User
from data.additional import bad_site, get_menu_btns
from threading import Thread

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

from data.api import passing_api, login_api


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.errorhandler(404)
def not_found(_):
    """Если страница не найдена"""
    return bad_site(404, title="Такой страницы нет", message="Страница не найдена")


@app.route("/")
def empty():
    """Просто страница для перенаправления"""
    return redirect("/passings")


@app.route("/about")
def about():
    """Страница об общих сведениях"""
    return render_template("about.html", title="О проекте", menu=get_menu_btns())


def main():
    db_session.global_init("db/labirint.db")
    app.register_blueprint(passing_api.blueprint)
    app.register_blueprint(login_api.blueprint)
    app.run(host='0.0.0.0', port=80)


def start():
    t = Thread(target=main)
    t.start()


if __name__ == '__main__':
    main()
