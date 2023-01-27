from flask import Flask, Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

from .forms import LoginForm, RegisterForm
from .models import Users
from . import db

auth = Blueprint('auth', __name__)

app = Flask(__name__)
bcrypt = Bcrypt(app)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                flash('Logged in successfully!', category='success')
                login_user(user)
                return redirect(url_for('views.index'))
        else:
            flash('Email does not exist.', category='error')
    
    return render_template("auth/login.html", user=current_user, form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = Users(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash('Account created!', category='success')
        return redirect(url_for('views.profile'))
    
    return render_template('auth/register.html', form=form)

@auth.route('/reset-password')
def reset_password():
    return render_template('auth/reset-password.html')