import logging
from flask import Flask, flash, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from datetime import datetime
from flask_login import login_manager, login_required
from tennisRanking.models import User, Matches, db
from tennisRanking.views.views import *
from tennisRanking.views.admin_views import *

app = Flask('tennisRanking')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_BINDS'] = {
    'matches' :'sqlite:///matches.db',
    'users': 'sqlite:///users.db'}
app.config['SECRET_KEY'] = "random string"

db.init_app(app)

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


with app.app_context():
    db.create_all()

@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.get(user_id)


# map the functions to basic URLs
app.add_url_rule('/', view_func=index, methods=['GET','POST'])
app.add_url_rule('/challenge/', view_func=challengePage, methods=['GET','POST'])
app.add_url_rule('/challenge/<int:id>+<int:myself_id>', view_func=challenge, methods=['GET','POST'])
app.add_url_rule('/challenge/<int:id>', view_func=myself, methods=['GET'])
app.add_url_rule('/resolve/', view_func=resolve, methods=['GET', 'POST'])
app.add_url_rule('/stats/', view_func=stats, methods=['GET', 'POST'])

# mat the functions to admin urls
app.add_url_rule('/admin/', view_func=admin, methods=['POST','GET'])
app.add_url_rule('/admin/delete/<int:id>', view_func=deletePlayer, methods=['POST','GET'])
app.add_url_rule('/admin/update/<int:id>', view_func=updatePlayer, methods=['POST'])
app.add_url_rule('/admin/delete/delete_all_matches', view_func=deleteMatchHistory, methods=['POST'])










