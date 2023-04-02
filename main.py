from flask import Flask, render_template, redirect, make_response, jsonify
from data import db_session
from data.users import User
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from forms.user import LoginForm, RegisterForm, make_settings_form
from flask_restful import reqparse, abort, Api, Resource
from data import users_resource
from flask_ngrok import run_with_ngrok
from data import ending_api

app = Flask(__name__)
run_with_ngrok(app)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(ending_api.blueprint)
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register_login_settings.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают", func=1)
        # func = 2 - изменение настроек
        # func = 1 - регистрация
        # func = 0 - авторизация
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.name == form.name.data).first():
            return render_template('register_login_settings.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть", func=1)
        user = User(name=form.name.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register_login_settings.html', title='Регистрация', form=form, func=1)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_authenticated:
        form = LoginForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.name == form.name.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect("/")
            return render_template('register_login_settings.html',
                                   message="Неправильный логин или пароль",
                                   form=form, func=0)
        return render_template('register_login_settings.html', title='Авторизация', form=form, func=0)
    return redirect("/")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route("/", methods=['GET', 'POST'])
@login_required
def settings_page():
    form = make_settings_form(current_user.hardness)
    if form.validate_on_submit():
        dbs = db_session.create_session()
        user = dbs.query(User).get(current_user.id)
        user.hardness = form.hardness.data
        dbs.commit()
    return render_template("register_login_settings.html", title="Настройки", form=form, func=2)


if __name__ == '__main__':
    main()
