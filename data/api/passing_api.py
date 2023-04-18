import flask
from flask import render_template

from data import db_session
from data.tables.reviews import Review
from data.tables.passings import Passing
from forms.ending import EndingForm
from forms.passings import SortForm
from data.api.login_api import need_login, current_user

from random import choice

from data.additional import bad_site, get_menu_btns


blueprint = flask.Blueprint(
    'passing_api',
    __name__,
    template_folder='templates'
)


@blueprint.route("/passings/<int:passing_id>", methods=["GET", "POST"])
@need_login
def get_passing(passing_id):
    """Страница с одним прохождением и комментариями к проекту"""
    dbs = db_session.create_session()
    passing = dbs.query(Passing).get(passing_id)
    if not passing or passing.username != current_user.name:
        return bad_site(message="Такой концовки нет или она не ваша")
    user = passing.user
    ending = passing.ending
    form = EndingForm()
    if form.validate_on_submit():
        review = Review(
            ending_id=ending.id,
            user_id=user.id,
            text=form.comment.data,
            mark=int(form.slider.data)
        )
        dbs.add(review)
        dbs.commit()
    return render_template("ending.html", user=user, ending=ending,
                           reviews=dbs.query(Review).all()[::-1], form=form, title=ending.name,
                           menu=get_menu_btns())


@blueprint.route("/passings", methods=["GET", "POST"])
@blueprint.route("/", methods=["GET", "POST"])
@need_login
def get_passings():
    """Страница со всеми прохождениями пользователя"""
    dbs = db_session.create_session()
    form = SortForm()
    func = {"id": lambda x: x.id,
            "названию": lambda x: x.ending.name,
            "дате": lambda x: x.date}[form.type.data]
    passings = sorted(dbs.query(Passing).filter(Passing.username == current_user.name).all(),
                      key=func, reverse=form.reverse.data)
    return render_template("passings.html", title="Прохождения", passings=passings,
                           menu=get_menu_btns(),
                           choice=choice([passing.id for passing in passings]) if passings else None,
                           form=form)
