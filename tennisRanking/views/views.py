from flask import Flask, flash, render_template, request, redirect
from flask_login import login_required
from tennisRanking.models import User, Matches, db
#from tennisRanking import app

# This route will display all players and ask you to select yourself.
# Step 1 in the challenge process. 
@login_required
def index():
    players = User.query.order_by(User.lastName).all()
    return render_template('index.html', players=players)
    

#This route will display all players besides yourself and ask you to select
#Who you want to challenge. Upon selecting the challenge, it will update the 
#DB with the availability of both players
@login_required
def challengePage():
    myself = User.query.get_or_404(id)
    players = User.query.order_by(User.lastName).all()
    return render_template('challenge.html', players=players, me=myself)

@login_required
def challenge(id,myself_id):
    challenging_player = User.query.get_or_404(myself_id)
    player_to_challenge = User.query.get_or_404(id)

    challenging_player.isAvailable = False
    player_to_challenge.isAvailable = False

    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue challenging'

@login_required
def myself(id):
    myself = User.query.get_or_404(id)
    players = User.query.order_by(User.lastName).all()
    return render_template('challenge.html', players=players, myself=myself)

@login_required
def resolve():
    if request.method == 'POST':
        # try:
        player_one_id = request.form.get('player_one')
        player_two_id = request.form.get('player_two')

        score = request.form.get('score')

        resolved_match = Matches(playerIdOne=player_one_id, playerIdTwo=player_two_id, matchScore=score, winner=player_one_id)
        
        db.session.add(resolved_match)
        db.session.commit()

        player_one = User.query.get_or_404(player_one_id)
        player_two = User.query.get_or_404(player_two_id)

        player_one.isAvailable = True
        player_two.isAvailable = True
        db.session.commit()
        return redirect('/resolve')
        # except:
        #     return 'There was an issue resolving this match. Try again then talk to Coach'

    else:
        players = User.query.order_by(User.lastName).all()
        return render_template('resolve.html', players=players)

@login_required
def stats():
    matches = Matches.query.all()
    players = User.query.order_by(User.lastName).all()


    # set up db so that player IDs are 

    # compare the IDs from the match db to the player DB -> brute force it for now teams are small
    # replace id with names? [id_1][id_2] -> [Ryan Smith][Josh Smith]

    # when it matches, print both. 
    return render_template('stats.html', matches=matches, players = players)