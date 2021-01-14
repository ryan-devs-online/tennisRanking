from flask import Flask, flash, render_template, request, redirect
from tennisRanking.models import User, Matches, db
from tennisRanking import app


#Admin stuff
@app.route('/admin/', methods=['POST','GET'])
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

        new_player = User(lastName=lName, firstName=fName, isAvailable=True, ranking=rank)
        try:
            db.session.add(new_player)
            db.session.commit()
            return redirect('/admin')
        except:
            return 'There was an issue adding this player. Try again, then talk to Ryan.'

    else:
        players = User.query.order_by(User.lastName).all()
        return render_template('admin.html', players=players)    

   
@app.route('/admin/delete/<int:id>')
def deletePlayer(id):
    player_to_delete = User.query.get_or_404(id)

    try:
        db.session.delete(player_to_delete)
        db.session.commit()
        return redirect('/admin')
    except:
        return 'There was a problem deleting'

@app.route('/admin/update/<int:id>')
def updatePlayer(id):
    player_to_update = User.query.get_or_404(id)

    # try:
    #      db.session.delete(task_to_delete)
    #      db.session.commit()
    #     return redirect('/')
    # except:
    return "I haven't finished this part yet"

@app.route('/admin/delete/delete_all_matches')
def deleteMatchHistory():
    Matches.query.delete()
    db.session.commit()
    return redirect('/admin')
