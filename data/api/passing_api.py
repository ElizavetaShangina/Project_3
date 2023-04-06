import flask
from flask import render_template, abort

from data import db_session
from data.tables.users import User
from data.tables.endings import Ending
from data.tables.reviews import Review
from data.tables.passings import Passing
from forms.ending import EndingForm
from data.api.login_api import need_login, current_user


blueprint = flask.Blueprint(
    'passing_api',
    __name__,
    template_folder='templates'
)


@blueprint.route("/passings/<int:passing_id>", methods=["GET", "POST"])
@need_login
def get_passing(passing_id):
    dbs = db_session.create_session()
    passing = dbs.query(Passing).get(passing_id)
    if not passing:
        abort(400)
    user = passing.user
    ending = passing.ending
    form = EndingForm()
    if form.validate_on_submit():
        review = Review(
            ending_id=ending_id,
            user_id=user_id,
            text=form.comment.data
        )
        dbs.add(review)
        dbs.commit()
    return render_template("ending.html", user=user, ending=ending,
                           reviews=dbs.query(Review).all(), form=form, title=ending.name)


@blueprint.route("/passings")
@need_login
def get_passings():
    dbs = db_session.create_session()
    passings = sorted(dbs.query(Passing).filter(Passing.username == current_user.name).all(),
                      key=lambda x: x.date, reverse=True)
    return render_template("passings.html", title="Прохождения", passings=passings)