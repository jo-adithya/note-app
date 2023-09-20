from flask import request, flash, render_template, redirect, url_for, jsonify
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, ForgotForm, ResetPasswordForm, AccountForm
from app.models import User, Note
import smtplib
import ssl
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from datetime import datetime
from random import randint
load_dotenv()
import os


@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
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
        return redirect(url_for('register'))

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
    notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.updatedAt.desc()).all()
    return render_template('home.html', title='All Notes', notes=notes, user=current_user)

@app.route('/notes/<id>', methods=['GET', 'PATCH'])
@login_required
def note(id):
    if request.method == 'GET':
        note = Note.query.get(id)
        if note is None:
            return redirect(url_for('index'))
        return render_template('note.html', title=note.title, note=note, user=current_user)
    if request.method == 'PATCH':
        note = Note.query.get(id)
        if note is None:
            return jsonify({'message': 'Note not found'}), 404

        data = request.get_json()
        title = data.get('title')
        body = data.get('body')

        # Perform the update in the database
        note.title = title
        note.body = body
        db.session.commit()

        return jsonify({'message': 'Note updated successfully'}), 200
    pass


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


def send_mail(user, form):
    token = user.get_token()

    smtp_port = 587
    smtp_server = "smtp.gmail.com"
    email_from = os.getenv("EMAIL")
    email_to = form.email.data
    pswd = os.getenv("PASSWORD")

    subject = "Password Recovery"
    body = f"Hello,\n\nPlease find your password recovery link below.\n\n{url_for('reset_token', token=token,_external=True)}\n\nRegards,\nYour team"
    message = f"Subject: {subject}\n\n{body}"

    simple_email_context = ssl.create_default_context()
    TIE_server = smtplib.SMTP(smtp_server, smtp_port)
    TIE_server.starttls(context=simple_email_context)
    TIE_server.login(email_from, pswd)
    TIE_server.sendmail(email_from, email_to, message)
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

    if form.password.data != form.confirmPass.data:
        flash('passwords do not match', 'warning')
        return redirect(url_for('reset_token', token=token))

    if form.validate_on_submit():
        userdb = User.query.filter_by(id=user).first()
        userdb.set_password(form.password.data)
        db.session.commit()
        flash("password successfully changed", 'success')
        return redirect(url_for('login'))
    return render_template('reset_pass.html', title="change password", legend="change password", form=form)

@app.route('/create', methods=['POST'])
def insert_data():
    try:
        # Insert data into the database
        id = randint(0, 99999999)
        note = Note(id=id, title="Notes", body="start typing", user_id=current_user.id)
        db.session.add(note)
        db.session.commit()
        
        # Return a JSON response indicating success
        response = {'status': 'success'}
        return jsonify(response)
    except Exception as e:
        print('Error inserting data:', e)

        response = {'status': 'error'}
        return jsonify(response)

@app.route('/delete', methods=['DELETE'])
def delete_note():
    note_id = request.args.get('id')
    note = Note.query.get(note_id)

    if note:
        db.session.delete(note)
        db.session.commit()
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False}), 404


@app.route('/user', methods=['GET', 'POST'])
def user():
    form = AccountForm()
    if(request.method == 'GET'):
        return render_template('user.html', user=current_user, form=form)   
    
    if(request.method == 'POST'):
        password = form.changePass.data
        confirm_password = form.confirmChangePass.data

        if password != confirm_password:
            flash('Passwords do not match', 'warning')
            return redirect(url_for('user'))
        else:
            userDB = User.query.filter_by(id=current_user.id).first()
            userDB.set_password(password)
            db.session.commit()
            flash('Password changed successfully', 'success')
            return redirect(url_for('user'))          
        
            