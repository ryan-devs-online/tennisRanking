import logging
from flask import Flask, flash, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///players.db'
app.config['SQLALCHEMY_BINDS'] = {
    'matches' :'sqlite:///matches.db',
    'players': 'sqlite:///players.db'}
app.config['SECRET_KEY'] = "random string"

#db = SQLAlchemy(app)


logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

db.create_all()


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.get(user_id)


# This route will display all players and ask you to select yourself.
# Step 1 in the challenge process. 
@app.route('/', methods=['POST','GET'])
def index():
    players = Players.query.order_by(Players.lastName).all()
    return render_template('index.html', players=players)
    
#Admin stuff
@app.route('/admin/', methods=['POST','GET'])
@login_required
def admin():
    # get user
    """
    if user is not a coach, don't allow to proceede and redirect 
    to a different page
    """
    if request.method == 'POST':
        fName = request.form['firstName']
        lName = request.form['lastName']
        rank = request.form['ranking']

        new_player = Players(lastName=lName, firstName=fName, isAvailable=True, ranking=rank)
        try:
            db.session.add(new_player)
            db.session.commit()
            return redirect('/admin')
        except:
            return 'There was an issue adding this player. Try again, then talk to Ryan.'

    else:
        players = Players.query.order_by(Players.lastName).all()
        return render_template('admin.html', players=players)    

   
@app.route('/admin/delete/<int:id>')
def deletePlayer(id):
    player_to_delete = Players.query.get_or_404(id)

    try:
        db.session.delete(player_to_delete)
        db.session.commit()
        return redirect('/admin')
    except:
        return 'There was a problem deleting'

@app.route('/admin/update/<int:id>')
def updatePlayer(id):
    player_to_update = Players.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem updating'

@app.route('/admin/delete/delete_all_matches')
def deleteMatchHistory():
    Matches.query.delete()
    db.session.commit()
    return redirect('/admin')


#This route will display all players besides yourself and ask you to select
#Who you want to challenge. Upon selecting the challenge, it will update the 
#DB with the availability of both players

@app.route('/challenge/',  methods=['GET','POST'])
def challengePage():
    mesup = Players.query.get_or_404(id)
    players = Players.query.order_by(Players.lastName).all()
    return render_template('challenge.html', players=players, me=myself)

@app.route('/challenge/<int:id>+<int:myself_id>', methods=['GET','POST'])
def challenge(id,myself_id):
    challenging_player = Players.query.get_or_404(myself_id)
    player_to_challenge = Players.query.get_or_404(id)

    challenging_player.isAvailable = False
    player_to_challenge.isAvailable = False

    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue challenging'

    return render_template('challenge.html', players=players)


@app.route('/challenge/<int:id>', methods=['GET'])
def myself(id):
    myself = Players.query.get_or_404(id)
    players = Players.query.order_by(Players.lastName).all()
    return render_template('challenge.html', players=players, myself=myself)

@app.route('/resolve/', methods=['GET', 'POST'])
def resolve():
    if request.method == 'POST':
        print("in the post")
        # try:
        print("in the try")
        player_one_id = request.form.get('player_one')
        player_two_id = request.form.get('player_two')

        score = request.form.get('score')

        resolved_match = Matches(playerIdOne=player_one_id, playerIdTwo=player_two_id, matchScore=score, winner=player_one_id)
        
        db.session.add(resolved_match)
        db.session.commit()

        player_one = Players.query.get_or_404(player_one_id)
        player_two = Players.query.get_or_404(player_two_id)

        player_one.isAvailable = True
        player_two.isAvailable = True
        db.session.commit()
        return redirect('/resolve')
        # except:
        #     return 'There was an issue resolving this match. Try again then talk to Coach'

    else:
        players = Players.query.order_by(Players.lastName).all()
        return render_template('resolve.html', players=players)


@app.route('/stats/', methods=['GET', 'POST'])
def stats():
    matches = Matches.query.all()
    players = Players.query.order_by(Players.lastName).all()


    # set up db so that player IDs are 

    # compare the IDs from the match db to the player DB -> brute force it for now teams are small
    # replace id with names? [id_1][id_2] -> [Ryan Smith][Josh Smith]

    # when it matches, print both. 



    return render_template('stats.html', matches=matches, players = players)


if __name__ == "__main__":
    app.run(debug=True)