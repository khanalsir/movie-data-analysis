# manage.py

from flask import Flask
from flask.cli import FlaskGroup
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db

app = create_app()
cli = FlaskGroup(create_app=lambda _: app)

migrate = Migrate(app, db)
cli.add_command('db', MigrateCommand)

if __name__ == '__main__':
    cli()
