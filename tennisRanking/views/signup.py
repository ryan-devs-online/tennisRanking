from flask import Flask, flash, render_template, redirect, url_for, request
from flask_login import login_user, login_required, current_user, logout_user
from tennisRanking.models import User, db, playerRanking
from werkzeug.security import generate_password_hash

def signup():
    if request.method == 'POST':
        fName = request.form['firstName']
        lName = request.form['lastName']
        email = request.form['email']
        password = request.form['password']

        hashedPass = generate_password_hash(password)

        new_player = User(lastName=lName, firstName=fName, isAvailable=True, ranking=playerRanking.unranked.value, email=email,
            isCoach=False, password=hashedPass, playingAgainst=None)
        try:
            db.session.add(new_player)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding this player. Try again, then talk to Ryan.'
    return render_template('signup.html')