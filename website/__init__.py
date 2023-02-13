from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://admin:gebongkalol@gebongka.c0yrjbkoofev.ap-southeast-1.rds.amazonaws.com/gebongka"
    app.config['SECRET_KEY'] = 'secretkey'
    db.init_app(app)

    from .auth import auth
    from .past_history import past_history
    from .views import views

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(past_history, url_prefix='/')

    from .models import Users

    with app.app_context():
        db.create_all()
        print("created db!")

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    return app