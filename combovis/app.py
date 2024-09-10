from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5
from flask_wtf.csrf import CSRFProtect
import secrets

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///combovis.db'
    app.secret_key = secrets.token_urlsafe(16)

    bootstrap = Bootstrap5(app)
    csrf = CSRFProtect(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    from .blueprints.auth.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from combovis.blueprints.core.routes import core
    from combovis.blueprints.combo.routes import combo
    from combovis.blueprints.auth.routes import auth_bp

    app.register_blueprint(core, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(combo, url_prefix='/combo')

    migrate = Migrate(app, db)

    return app
