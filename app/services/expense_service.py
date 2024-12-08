from app.models.models import Expense
from app import db
from sqlalchemy import func

class ExpenseService:
    def add_expense(self, user_id, amount, day_id):
        expense = Expense(
            amount=amount,
            user_id=user_id,
            day_id=day_id
        )

        db.session.add(expense)
        db.session.commit()

        return expense

    def get_daily_totals(self, user_id):
        # Querys day_id and sum of expenses
        daily_totals = db.session.query(Expense.day_id, func.sum(Expense.amount).label('total'))

        # Filters by user and group them by day
        daily_totals = daily_totals.filter_by(user_id=user_id).group_by(Expense.day_id)

        # Execute the query
        daily_totals = daily_totals.all()

        return daily_totals

    def clear_expenses(self, user_id):
        Expense.query.filter_by(user_id=user_id).delete()
        db.session.commit()

    def get_user_expenses(self, user_id):
        return Expense.query.filter_by(user_id=user_id).all()