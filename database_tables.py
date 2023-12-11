from app import create_app, db

app = create_app()

# Run this command to create the tables
with app.app_context():
    db.create_all()
