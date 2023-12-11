from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user

from app import db, login_manager
from app.models import User

routes = Blueprint('routes', __name__)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@routes.route('/')
def home():
    return render_template('home.html')


@routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already registered. Please sign in.')
            return redirect(url_for('routes.signin'))

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('User successfully registered. Please sign in.')
        return redirect(url_for('routes.signin'))

    return render_template('signup.html')


@routes.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            login_user(user)
            return redirect(url_for('routes.dashboard'))
        else:
            flash('Invalid email or password. Please try again.')

    return render_template('signin.html')


@routes.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('routes.home'))


@routes.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

