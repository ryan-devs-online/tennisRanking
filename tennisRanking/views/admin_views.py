from flask import Flask, flash, render_template, request, redirect
from tennisRanking.models import User, Matches, db


def admin():
    """
    if user is not a coach, don't allow to proceede and redirect 
    to a different page
    """
    if request.method == 'POST':
        fName = request.form['firstName']
        lName = request.form['lastName']
        rank = request.form['ranking']
        isCoach = request.args.get('isCoach')


        new_player = User(lastName=lName, firstName=fName, isAvailable=True, ranking=rank, isCoach=isCoach)
        try:
            print("in the try")
            db.session.add(new_player)
            db.session.commit()
            return redirect('/admin')
        except:
            return 'There was an issue adding this player. Try again, then talk to Ryan.'

    else:
        players = User.query.order_by(User.lastName).all()
        return render_template('admin.html', players=players)    

   
def deletePlayer(id):
    player_to_delete = User.query.get_or_404(id)

    try:
        db.session.delete(player_to_delete)
        db.session.commit()
        return redirect('/admin')
    except:
        return 'There was a problem deleting'

def updatePlayer(id):
    player_to_update = User.query.get_or_404(id)

    # try:
    #      db.session.delete(task_to_delete)
    #      db.session.commit()
    #     return redirect('/')
    # except:
    return "I haven't finished this part yet"

def deleteMatchHistory():
    Matches.query.delete()
    db.session.commit()
    return redirect('/admin')
