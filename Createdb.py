from app import app, db

# Create an application context
with app.app_context():
    # Now you can perform database operations
    db.create_all()
