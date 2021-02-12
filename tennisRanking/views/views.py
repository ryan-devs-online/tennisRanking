from flask import Flask, flash, render_template, request, redirect
from flask_login import login_required, current_user
from tennisRanking.models import User, Matches, db

@login_required
def index():
    if not current_user.isAvailable:
        opponent =User.query.get_or_404(current_user.playingAgainst)
        return render_template('resolve.html', current_user=current_user, opponent=opponent)
    else:
        players = User.query.order_by(User.lastName).all()
        return render_template('index.html', players=players)

@login_required
def personal():
    players = User.query.order_by(User.lastName).all()
    matchesOne = Matches.query.filter(Matches.playerIdOne==current_user.userId).all()
    matchesTwo = Matches.query.filter(Matches.playerIdTwo==current_user.userId).all()
    matches = matchesOne + matchesTwo
    return render_template('personal.html', matches=matches, current_user = current_user, players=players)
    
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
    if request.method == 'POST':
        opponent =User.query.get_or_404(current_user.playingAgainst)
        winner = request.form.get('winner')

        score = request.form.get('score')

        resolved_match = Matches(playerIdOne=current_user.userId, playerIdTwo=current_user.playingAgainst, matchScore=score, winner=winner)

        current_user.isAvailable = True
        opponent.isAvailable = True
        current_user.playingAgainst = None
        opponent.playingAgainst = None

        db.session.add(resolved_match)
        db.session.commit()
        return redirect('/')

    else:
        return render_template('resolve.html', current_user=current_user, opponent=None)

@login_required
def dispute(matchId):
    match = Matches.query.get(matchId)
    if current_user.userId != match.playerIdOne and current_user != match.playerIdTwo:
        return "Nice Try nerd"
    else:            
        match.isDisputed = True
        db.session.commit()
    return redirect('/personal/')
        # return render_template('personal.html')

@login_required
def stats():
    matches = Matches.query.all()
    players = User.query.order_by(User.lastName).all()
    return render_template('stats.html', matches=matches, players = players)
