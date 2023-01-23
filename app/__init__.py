from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from config import Config
from sqlalchemy import MetaData


convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)


app = Flask(__name__)
app.config.from_object(Config)


bootstrap = Bootstrap(app)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db, render_as_batch=True)
login = LoginManager(app)
login.login_view = 'login'
moment = Moment(app)


from app import routes, models, errors
