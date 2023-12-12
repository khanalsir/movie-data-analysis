from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user

from app import db, login_manager
from app.models import User, Movie, Review
from app.services.MovieDataExtractor import MovieDataExtractor

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
    flash('You have been signed out.', 'success')
    return redirect(url_for('routes.home'))


@routes.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@routes.route('/movies', methods=['GET', 'POST'])
def movies():
    # Extract movies for the current year (you can customize this)
    movies_info = MovieDataExtractor.extract_all_movies()
    print(movies_info)
    if request.method == 'POST':
        # Handle form submission or filtering if needed
        return render_template('movies.html', movies=movies_info)

    return render_template('movies.html', movies=movies_info)


@routes.route('/movie_detail/<imdb_id>')
@login_required
def movie_detail(imdb_id):
    movie = Movie.query.filter_by(imdb_id=imdb_id).first()
    return render_template('movie_detail.html', movie=movie)


@routes.route('/my_movies')
@login_required
def my_movies():
    reviews = Review.query.filter_by(user_id=current_user.id).all()
    return render_template('my_movies.html', reviews=reviews)

