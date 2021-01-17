from flask import Flask, flash, render_template, redirect, url_for, request
from flask_login import login_user, login_required, current_user, logout_user
from tennisRanking.models import User, db
from werkzeug.security import check_password_hash

def login():
    if current_user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
            email = request.form['email']
            user = User.query.filter_by(email = email).first()
            if user is not None and user.check_password(request.form['password']):
                login_user(user)
                return redirect('/blogs')
        
    return render_template('login.html')
    
    # if form.validate_on_submit():
    #     user = User.query.get(form.email.data)
    #     if user:
    #         if check_password_hash(user.password, form.password.data):
    #             user.authenticated = True
    #             db.session.add(user)
    #             db.session.commit()
    #             login_user(user, remember=True)
    #             return redirect(url_for("index.html"))
    # return render_template("login.html", form=form)

@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return render_template("logout.html")