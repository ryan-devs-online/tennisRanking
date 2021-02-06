from flask import Flask, flash, render_template, redirect, url_for, request, session
from flask_login import login_user, login_required, current_user, logout_user
from functools import wraps
from tennisRanking.models import User, db
from werkzeug.security import check_password_hash

def login():
    if current_user.is_authenticated:
        return redirect(session["wants_url"])

    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email = email).first()
        if user is not None and user.check_password(request.form['password']):
            user.authenticated = True
            isLogin = login_user(user, remember=True)
            db.session.add(user)
            db.session.commit()

            next = request.args.get('next')

            return redirect('/')
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
    outLog = logout_user()
    print("log out : " + str(outLog))
    return render_template("logout.html")