from flask import make_response, render_template, request
from flask_login import current_user
from random import choice


def get_menu_btns():
    address = request.path[1:]
    btns = []
    if current_user.is_authenticated:
        if address != "passings":
            btns.append("Концовки")
        btns.append("Выйти")
    else:
        if address != "login":
            btns.append("Войти")
        if address != "register":
            btns.append("Зарегистрироваться")
    if address != "about":
        btns.append("О нас")
    return btns


titles = [":(", "Что-то пошло не так...", "Опять, не так", "("]


def bad_site(code=400, **kwargs):
    add_kwargs = {}
    if "title" not in kwargs:
        add_kwargs["title"] = choice(titles)
    return make_response(render_template("bad_site.html", **kwargs | add_kwargs,
                                         menu=get_menu_btns()), code)
