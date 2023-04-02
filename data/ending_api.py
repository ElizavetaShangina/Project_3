import flask
from flask import render_template

from .resources_parsers import ending_parser
from . import db_session
from .users import User
from .endings import Ending
from .reviews import Review
from forms.ending import EndingForm


blueprint = flask.Blueprint(
    'ending_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/ending', methods=["POST"])
def get_ending():
    dbs = db_session.create_session()
    args = ending_parser.parse_args()
    user = dbs.query(User).get(args["user_id"])
    ending = dbs.query(Ending).get(args["ending_id"])
    rating = args["rating"]
    form = EndingForm()
    if form.validate_on_submit():
        review = Review(
            ending_id=ending_id,
            user_id=user_id,
            text=form.comment.data
        )
        dbs.add(review)
        dbs.commit()
    return render_template("ending.html", rating=rating, user=user, ending=ending,
                           reviews=dbs.query(Review).all(), form=form)


# @blueprint.route("/ending/<int:ending_id>/<int:user_id>/<float:rating>", methods=["GET", "POST"])
# def get_ending_2(ending_id, user_id, rating):
#     dbs = db_session.create_session()
#     user = dbs.query(User).get(user_id)
#     ending = dbs.query(Ending).get(ending_id)
#     form = EndingForm()
#     if form.validate_on_submit():
#         review = Review(
#             ending_id=ending_id,
#             user_id=user_id,
#             text=form.comment.data
#         )
#         dbs.add(review)
#         dbs.commit()
#     return render_template("ending.html", rating=rating, user=user, ending=ending,
#                            reviews=dbs.query(Review).all(), form=form)
