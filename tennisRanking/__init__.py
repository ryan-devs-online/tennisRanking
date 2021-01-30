import logging

from datetime import datetime
from flask import Flask, flash, render_template, request, redirect
from flask_login import LoginManager, login_manager, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from tennisRanking.models import User, Matches, db
from tennisRanking.views.views import *
from tennisRanking.views.admin_views import *
from tennisRanking.views.loginManager import *
from tennisRanking.views.signup import *

app = Flask('tennisRanking')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_BINDS'] = {
    'matches' :'sqlite:///matches.db',
    'users': 'sqlite:///users.db'}
app.config['SECRET_KEY'] = "random string"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db.init_app(app)

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


with app.app_context():
    db.create_all()


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

# map the functions to basic URLs
app.add_url_rule('/', view_func=index, methods=['GET','POST'])
app.add_url_rule('/challenge/', view_func=challengePage, methods=['GET','POST'])
app.add_url_rule('/challenge/<int:id>+<int:myself_id>', view_func=challenge, methods=['GET','POST'])
app.add_url_rule('/challenge/<int:id>', view_func=myself, methods=['GET'])
app.add_url_rule('/resolve/', view_func=resolve, methods=['GET', 'POST'])
app.add_url_rule('/stats/', view_func=stats, methods=['GET', 'POST'])

# map the functions to admin urls
app.add_url_rule('/admin/', view_func=admin, methods=['POST','GET'])
app.add_url_rule('/admin/delete/<int:id>', view_func=deletePlayer, methods=['POST','GET'])
app.add_url_rule('/admin/update/<int:id>', view_func=updatePlayer, methods=['POST'])
app.add_url_rule('/admin/delete/delete_all_matches', view_func=deleteMatchHistory, methods=['POST'])

# map the login / logout stuff
app.add_url_rule('/login/', view_func=login, methods=['POST','GET'])
app.add_url_rule('/logout/', view_func=logout, methods=['POST','GET'])

# map the signup
app.add_url_rule('/signup/', view_func=signup, methods=['POST', 'GET'])












