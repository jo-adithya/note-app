from flask import render_template
from app import app
from .forms import LoginForm

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

@app.route('/register')
def register():
    form = LoginForm()
    return render_template('register.html', form=form)

@app.route('/')
def forgot():
    form = LoginForm()
    return render_template('forgot.html', form=form)