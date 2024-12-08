from app.models.models import User
from app import db, bcrypt

class UserService:
    def create_user(self, username, password):
        hashed_password = bcrypt.generate_password_hash(password)
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return user

    def get_user_by_username(self, username):
        # Querys the database for a user with the username
        return User.query.filter_by(username=username).first()

    def verify_password(self, user, password):
        return bcrypt.check_password_hash(user.password, password)

    def update_budget(self, user, budget, reset=False):
        user.budget = budget
        if reset:
            user.day = 1
        db.session.commit()
        return user

    def increment_day(self, user):
        user.day += 1
        db.session.commit()
        return user.day

    def get_budget(self, user_id):
        user = User.query.get(user_id)
        return user.budget if user else None