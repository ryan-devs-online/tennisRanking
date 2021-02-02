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
    update_player = User.query.get_or_404(id)
    if request.method == 'POST':
        print("in the POST  !!!!!!!!!!!!!!!!!! ")
        fName = request.form['firstName']
        lName = request.form['lastName']
        email = request.form['email']
        rank  = request.form['rank']

        update_player = User.query.get_or_404(id)
        update_player.fName = fName
        update_player.lName = lName
        update_player.email = email
        update_player.rank = rank

        try:
            db.session.commit()
            return render_template('admin.html')
        except:
            return 'There was an issue updating this player. Try again, then talk to Ryan.'
    else:
        return render_template('update.html', update_player=update_player)

@login_required
def submitPlayer():
    update_player = User.query.get_or_404(id)
    if request.method == 'POST':
        print("in the POST  !!!!!!!!!!!!!!!!!! ")
        fName = request.form['firstName']
        lName = request.form['lastName']
        email = request.form['email']
        rank  = request.form['rank']

        update_player = User.query.get_or_404(id)
        update_player.fName = fName
        update_player.lName = lName
        update_player.email = email
        update_player.rank = rank

        try:
            db.session.commit()
            return render_template('admin.html')
        except:
            return 'There was an issue updating this player. Try again, then talk to Ryan.'
    else:
        return render_template('admin.html')

@login_required
def deleteMatchHistory():
    Matches.query.delete()
    db.session.commit()
    return redirect('/admin')
