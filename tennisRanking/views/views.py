from flask import Flask, flash, render_template, request, redirect
from flask_login import login_required, current_user
from tennisRanking.models import User, Matches, db
#from tennisRanking import app

# This route will display all players and ask you to select yourself.
# Step 1 in the challenge process. 
@login_required
def index():
    players = User.query.order_by(User.lastName).all()
    return render_template('index.html', players=players)
    
@login_required
def challenge(id):
    player_to_challenge = User.query.get_or_404(id)

    current_user.isAvailable = False
    player_to_challenge.isAvailable = False

    current_user.playingAgainst = player_to_challenge.userId
    player_to_challenge.playingAgainst = current_user.userId

    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue challenging'

@login_required
def resolve():
    opponent =User.query.get_or_404(current_user.playingAgainst)
    if request.method == 'POST':
        winner = request.form.get('winner')

        score = request.form.get('score')

        resolved_match = Matches(playerIdOne=current_user.userId, playerIdTwo=current_user.playingAgainst, matchScore=score, winner=winner)

        current_user.isAvailable = True
        opponent.isAvailable = True
        db.session.add(resolved_match)
        db.session.commit()
        return redirect('/')

    else:
        opponent = User.query.get_or_404(current_user.playingAgainst)
        return render_template('resolve.html', current_user=current_user, opponent=opponent)

@login_required
def stats():
    matches = Matches.query.all()
    players = User.query.order_by(User.lastName).all()
    return render_template('stats.html', matches=matches, players = players)
