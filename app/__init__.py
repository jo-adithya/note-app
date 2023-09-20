import mimetypes
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

# Initialize Configurations
app.config.from_object(Config)

# Initialize Database Connection
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize Login Manager
login = LoginManager(app)
login.login_view = 'login'

# secretKey
app.config['SECRET_KEY']='resetkey'

from . import routes, models
