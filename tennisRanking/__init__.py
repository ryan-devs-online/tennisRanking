import logging
from flask import Flask, flash, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from datetime import datetime
from tennisRanking.models import User, Matches, db
# from tennisRanking.views import views
# from tennisRanking.views import admin_views

app = Flask('tennisRanking')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///players.db'
app.config['SQLALCHEMY_BINDS'] = {
    'matches' :'sqlite:///matches.db',
    'players': 'sqlite:///players.db'}
app.config['SECRET_KEY'] = "random string"


logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

db.create_all()


def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.get(user_id)


