from flask import Flask
from flask_login import LoginManager
# from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)

app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
# toolbar = DebugToolbarExtension(app)
mail = Mail(app)

login_manager = LoginManager(app)
login_manager.login_message = "Veillez vous connecter!"
login_manager.login_view = "auth.login"

from .entity.Article import Category, Article
from .entity.Message import Message
from .entity.Page import Page
from .entity.Video import Video
from .entity.User import User

from .admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from .front import front as front_blueprint
app.register_blueprint(front_blueprint)


from app.utils.filter import datetimeformat, startswith
app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['startswith'] = startswith
