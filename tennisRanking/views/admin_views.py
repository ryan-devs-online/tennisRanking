from flask import Flask, flash, render_template, request, redirect
from flask_login.utils import login_required
from flask_login import login_required
from tennisRanking.models import User, Matches, playerRanking, db

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
    player_update = User.query.get_or_404(id)
    return render_template('update.html', player=player_update, ranking=playerRanking)

@login_required
def submitPlayer(id):
    update_player = User.query.get_or_404(id)
    if request.method == 'POST':
        fName = request.form['firstName']
        lName = request.form['lastName']
        email = request.form['email']
        rank  = request.form['ranking']
        # coach = request.form['isCoach']
        # print("rank: " + str(rank))

        update_player.firstName = fName
        update_player.lastName = lName
        update_player.email = email
        update_player.ranking = rank

        try:
            db.session.commit()
            return redirect('/admin')
        except:
            return 'There was an issue updating this player. Try again, then talk to Ryan.'
    else:
        return render_template('admin.html')

@login_required
def deleteMatchHistory():
    Matches.query.delete()
    db.session.commit()
    return redirect('/admin')
