from app.models.models import Notification
from app import db
from datetime import datetime

class NotificationService:
    def create_notification(self, user_id, title, message):
        notification = Notification(
            user_id=user_id,    # Associate the notification with the current user
            title=title,
            message=message,
            created_at=datetime.now()   # Use the current time for the notification's creation
        )
        db.session.add(notification)
        db.session.commit()

        return notification

    def get_user_notifications(self, user_id):
        # Get all notifications
        return Notification.query.filter_by(
            user_id=user_id
        ).order_by(Notification.created_at.desc()).all()

    def create_budget_notification(self, user_id, budget, expense_amount=None):
        if expense_amount:
            title = "Running out of Budget"
            message = f"After your latest expense of ${expense_amount}, your budget is now ${budget}."
        else:
            title = "New Budget Set"
            message = f"You have set your budget to be ${budget}."
        
        return self.create_notification(user_id, title, message)