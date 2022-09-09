from flask import request, flash, render_template, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User


@app.route('/forget', methods=['GET', 'POST'])
def forget():
    return render_template('forgot.html', title='Forgot Password')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        # Data Verification
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return(redirect(url_for('login')))

        # Verified
        login_user(user, remember=form.remember_me.data)

        # Check if user requested a protected url before login
        requested_url = request.args.get('next')
        if not requested_url or url_parse(requested_url).netloc != '':
            requested_url = url_for('index')
        return redirect(requested_url)

    return render_template('login.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    user = User.query.filter_by(username=form.username.data).first()
    userEmail = User.query.filter_by(email=form.email.data).first()

    if user is not None or userEmail is not None:
        flash('Username or Email already exist!')
        return(redirect(url_for('register')))

    if form.validate_on_submit():
        # Add user to the database
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration Successful!")
        return redirect(url_for('login'))
    

    return render_template('register.html', title='Register', form=form)


@app.route('/')
@login_required
def index():
    return render_template('index.html', title='Notes')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
