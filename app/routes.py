from flask import request, flash, render_template, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, ForgotForm, ResetPasswordForm
from app.models import User
import smtplib
import ssl
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/forget', methods=['GET', 'POST'])
def forget():
    form = ForgotForm()
    try:
        return render_template('forgot.html', title='Forgot Password', form=form)
    except Exception as e:
        print(e)
        return str(e)


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


def send_mail(user, form):
    token = user.get_token()

    smtp_port = 587
    smtp_server = "smtp.gmail.com"
    email_form = "axelcornelius301@gmail.com"
    email_to = form.email.data
    pswd = "rarudwgqpglflljn"

    subject = "Password Recovery"
    body = f"Hello,\n\nPlease find your password recovery link below.\n\n{url_for('reset_token', token=token,_external=True)}\n\nRegards,\nYour team"
    message = f"Subject: {subject}\n\n{body}"

    simple_email_context = ssl.create_default_context()
    TIE_server = smtplib.SMTP(smtp_server, smtp_port)
    TIE_server.starttls(context=simple_email_context)
    TIE_server.login(email_form, pswd)
    TIE_server.sendmail(email_form, email_to, message)
    TIE_server.quit()


@app.route('/reset_password', methods=['GET','POST'])
def reset_password():
    form = ForgotForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user: 
            send_mail(user, form)
            flash('Reset request sent. Check your email')
            return redirect(url_for('login'))
    return render_template('forgot.html', title='reset password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user=User.verify_token(token)
    if user is None:
        flash('token invalid or expired. Please try again','warning')
        return redirect(url_for('reset_password'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        userdb = User.query.filter_by(id=user).first()
        userdb.set_password(form.password.data)
        db.session.commit()
        flash("password successfully changed", 'success')
        return redirect(url_for('login'))
    return render_template('reset_pass.html', title="change password", legend="change password", form=form)
