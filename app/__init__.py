from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mass.db'
    app.config['SECRET_KEY'] = '614cec5f63bbde733776f3752cf340f8'

    db.init_app(app)
    login_manager.init_app(app)

    from .routes import routes
    app.register_blueprint(routes)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
