from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash


db = SQLAlchemy()


class User(db.Model):
    __bind_key__ = 'users'
    userId = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)
    lastName = db.Column(db.String(15), nullable=False)
    firstName = db.Column(db.String(15), nullable=False)
    challengeDate = db.Column(db.DateTime, default=datetime.utcnow)
    isAvailable = db.Column(db.Boolean, nullable=False)
    ranking = db.Column(db.String, nullable=False)
    isCoach = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User %r>' % self.userId

    def is_active(self):
        return True
        
    def get_id(self):
        return chr(self.userId)

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_admin(self):
        return self.isCoach


# this should stay the same I think
class Matches(db.Model):
    __bind_key__ = 'matches'
    matchId = db.Column(db.Integer, primary_key=True)
    playerIdOne = db.Column(db.Integer, db.ForeignKey('players.playerId'), nullable=False)
    playerIdTwo = db.Column(db.Integer, db.ForeignKey('players.playerId'), nullable=False)
    matchScore = db.Column(db.String, nullable=False)
    winner = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Match %r>' % self.matchId