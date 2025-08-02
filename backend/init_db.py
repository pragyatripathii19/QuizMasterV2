from backend.models import db, User
from app import createApp  

app = createApp()  # Create a new app instance

with app.app_context():
    #db.drop_all()  #to get clean db everytime
    db.create_all()
    admin = User.query.filter_by(is_admin=True).first()
    if not admin:
        print("Creating default admin user...")
        admin = User(username='admin@example.com', is_admin=True)
        admin.password = 'adminpassword123'
        db.session.add(admin)
        db.session.commit()
    else:
        print("Admin already exists.")
