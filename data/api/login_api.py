import flask
from flask import render_template, redirect

from data import db_session
from data.tables.users import User
from data.tables.passings import Passing
from data.tables.combos import Combo
from forms.user import LoginForm, RegisterForm
from main import current_user, login_user, logout_user
from data.additional import bad_site, get_menu_btns


blueprint = flask.Blueprint(
    'login_api',
    __name__,
    template_folder='templates'
)


def need_login(func):
    """Проверка на авторизацию, с перенаправлением на страницу с авторизацией,
    если пользователь не авторизован"""
    def worker(*args, **kwargs):
        if current_user.is_authenticated:
            return func(*args, **kwargs)
        return redirect("/login")
    worker.__name__ = func.__name__
    return worker


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """Страница с регистрацией"""
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register_login.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают", menu=get_menu_btns())
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.name == form.name.data).first():
            return render_template('register_login.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть", menu=get_menu_btns())
        user = User(name=form.name.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register_login.html', title='Регистрация', form=form,
                           menu=get_menu_btns())


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Страница с авторизацией"""
    if not current_user.is_authenticated:
        form = LoginForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.name == form.name.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect("/passings")
            return render_template('register_login.html',
                                   message="Неправильный логин или пароль",
                                   form=form, menu=get_menu_btns())
        return render_template('register_login.html', title='Авторизация', form=form,
                               menu=get_menu_btns())
    return redirect("/passings")


@blueprint.route('/logout')
@need_login
def logout():
    """Выход из учетной записи"""
    logout_user()
    return redirect("/login")


@blueprint.route("/login_user/<string:combination>")
def log_user(combination):
    """Авторизация пользователя с помощью специального кода"""
    dbs = db_session.create_session()
    combo = dbs.query(Combo).filter(Combo.combo == combination).first()
    if combo:
        login_user(combo.user)
        dbs.delete(combo)
        dbs.commit()
        return redirect(f"/passings/{combo.passing_id}")
    else:
        return bad_site(message="Ссылка уже была использована или ссылка является неправильной")