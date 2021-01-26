from flask import Flask, flash, render_template, redirect, url_for, request
from flask_login import login_user, login_required, current_user, logout_user
from tennisRanking.models import User, db
from werkzeug.security import check_password_hash

def login():
    # if current_user.is_authenticated:
    #     return render_template('index.html')

    if request.method == 'POST':
            email = request.form['email']
            user = User.query.filter_by(email = email).first()
            if user is not None and user.check_password(request.form['password']):
                login_user(user, remember=True)
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                return render_template('index.html')
            return "Wrong password"
    if request.method == 'GET':
        return render_template('login.html')
    return render_template('error.html')    
    
    

@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return render_template("logout.html")