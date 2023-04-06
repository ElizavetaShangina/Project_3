import flask
from flask import render_template, abort

from data import db_session
from data.tables.users import User
from data.tables.endings import Ending
from data.tables.reviews import Review
from forms.ending import EndingForm


blueprint = flask.Blueprint(
    'ending_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/ending', methods=["GET", "POST"])
def get_ending():
    dbs = db_session.create_session()
    data = open("data/User_data.txt", encoding="utf-8").read().split()
    user = dbs.query(User).filter(User.name == data[0]).first()
    ending = dbs.query(Ending).filter(Ending.name == data[1]).first()
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
                           reviews=dbs.query(Review).all(), form=form)


@blueprint.route("/ending/<string:ending_name>/<string:user_name>", methods=["GET", "POST"])
def get_ending_2(ending_name, user_name):
    dbs = db_session.create_session()
    user = dbs.query(User).filter(User.name == user_name).first()
    ending = dbs.query(Ending).filter(Ending.name == ending_name).first()
    if not ending or not user:
        abort(400)
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
                           reviews=dbs.query(Review).all(), form=form)
