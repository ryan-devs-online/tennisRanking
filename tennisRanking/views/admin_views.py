from flask import Flask, flash, render_template, request, redirect
from flask_login.utils import login_required
from flask_login import login_required,current_user
from tennisRanking.models import User, Matches, playerRanking, db

@login_required
def admin():
    if current_user.isCoach:
        players = User.query.order_by(User.lastName).all()
        return render_template('admin.html', players=players)
    else:
        return redirect('/')

@login_required  
def deletePlayer(id):
    if current_user.isCoach:
        player_to_delete = User.query.get_or_404(id)

        try:
            db.session.delete(player_to_delete)
            db.session.commit()
            return redirect('/admin')
        except:
            return 'There was a problem deleting'
    else:
        return redirect('/')


@login_required
def updatePlayer(id):
    if current_user.isCoach:
        player_update = User.query.get_or_404(id)
        current_rank = player_update.ranking
        print("Current_rank: " + str(current_rank))
        return render_template('update.html', player=player_update, ranking=playerRanking, current_rank=current_rank)
    else:
        return redirect('/')

@login_required
def submitPlayer(id):
    if current_user.isCoach:
        update_player = User.query.get_or_404(id)
        if request.method == 'POST':
            fName = request.form['firstName']
            lName = request.form['lastName']
            email = request.form['email']
            rank  = request.form['ranking']
            coach = request.form.get("isCoach")
            
            if(fName == ""):
                fName = update_player.firstName
            if(lName == ""):
                lName = update_player.lastName
            if(email == ""):
                email = update_player.email
            if(coach == "on"):
                coach = True     
            
            update_player.firstName = fName
            update_player.lastName = lName
            update_player.email = email
            update_player.ranking = rank
            update_player.isCoach = coach

            try:
                db.session.commit()
                return redirect('/admin')
            except:
                return 'There was an issue updating this player. Try again, then talk to Ryan.'
        else:
            return render_template('admin.html')
    else:
        return redirect('/')

@login_required
def deleteMatchHistory():
    if current_user.isCoach:
        Matches.query.delete()
        db.session.commit()
        return redirect('/admin')
    else:
        return redirect('/')
