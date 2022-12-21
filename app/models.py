from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from app import db, login, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    notes = db.relationship('Note', backref='author', lazy='dynamic')

    def get_token(self, expires_sec = 300):
        serial = Serializer(app.config['SECRET_KEY'], expires_in=expires_sec)
        return serial.dumps({'user_id':self.id}).decode('utf-8 ')

    @staticmethod
    def verify_token(token):
        serial=Serializer(app.config['SECRET_KEY'])
        try:
            user_id = serial.loads(token)['user_id']
            return user_id
        except:
            return None

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True, unique=True)
    body = db.Column(db.Text)
    createdAt = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.title)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))