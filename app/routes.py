from flask import render_template, redirect, url_for
from app import app
from .forms import LoginForm

@app.route('/forget')
def forget():
    return render_template('forgot.html', title='Forgot Password')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if (form.validate_on_submit()):
        return redirect(url_for('index'))
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm()
    return render_template('register.html', title='Register', form=form)

@app.route('/')
def index():
    return render_template('index.html', title='Notes')