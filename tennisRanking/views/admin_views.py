from flask import Flask, flash, render_template, request, redirect
from flask_login.utils import login_required
from flask_login import login_required
from tennisRanking.models import User, Matches, db

@login_required
def admin():
    players = User.query.order_by(User.lastName).all()
    return render_template('admin.html', players=players)    

@login_required  
def deletePlayer(id):
    player_to_delete = User.query.get_or_404(id)

    try:
        db.session.delete(player_to_delete)
        db.session.commit()
        return redirect('/admin')
    except:
        return 'There was a problem deleting'

@login_required
def updatePlayer(id):
    player_to_update = User.query.get_or_404(id)
    return "I haven't finished this part yet"

@login_required
def deleteMatchHistory():
    Matches.query.delete()
    db.session.commit()
    return redirect('/admin')
