from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app.services.expense_service import ExpenseService
from app.services.user_service import UserService
from app.services.notification_service import NotificationService

# Initialize services
expense_service = ExpenseService()
user_service = UserService()
notification_service = NotificationService()

def init_routes(app):

    # Checks user's authentication status
    @app.route('/')
    def check_status():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        return redirect(url_for('login'))
    
    # Route for home page
    @app.route('/home')
    @login_required
    def home():
        return render_template('home.html')
    
    # Route for notifications page
    @app.route('/notifications')
    @login_required
    def notifications():
        return render_template('notifications.html')
    
    # Route for register page
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        # Runs if user submits the form
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            # Checks if the username is taken
            if user_service.get_user_by_username(username):
                # Shows the error message
                flash('Username has already been taken')

                return redirect(url_for('register'))
            
            # Creates a new user and add it to the database
            user_service.create_user(username, password)
            return redirect(url_for('login'))
        
        return render_template('register.html')
    
    # Route for login page
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        # Runs if user submits the form
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = user_service.get_user_by_username(username)

            # Logs the user in if username and password matches
            if user and user_service.verify_password(user, password):
                login_user(user)
                return redirect(url_for('home'))
            
            # Shows the error message
            flash("Invalid username or password!")
             
        return render_template('login.html')
    
    # Route for user logout
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('login'))
    
    # Route for tracking page
    @app.route('/track')
    @login_required
    def track():
        daily_totals = expense_service.get_daily_totals(current_user.uid)
        days = [day for day, _ in daily_totals]
        totals = [float(total) for _, total in daily_totals]

        return render_template('track.html', days=days, totals=totals)

    # Route for adding expenses
    @app.route('/add-expense', methods=['POST'])
    @login_required
    def add_expense():
        expense_amount = float(request.form.get('add-expense'))
        new_expense = expense_service.add_expense(
            user_id=current_user.uid,
            amount=expense_amount,
            day_id=current_user.day
        )

        # Update user's budget
        new_budget = current_user.budget - expense_amount
        user_service.update_budget(current_user, new_budget, reset=False)

        # Create notification if budget is low
        if new_budget <= 0:
            notification_service.create_notification(
                user_id=current_user.uid,
                title="Running out of Budget",
                message=f"After your latest expense of ${expense_amount}, your budget is now {new_budget}."
            )

        return jsonify({
            'id': new_expense.id, 
            'expense': new_expense.amount,
            'day_id': new_expense.day_id
        })

    # Route for increment onee day
    @app.route('/next-day', methods=['POST'])
    @login_required
    def next_day():
        new_day = user_service.increment_day(current_user)

        return jsonify({'day': new_day})
    
    # Route for get all expenses
    @app.route('/get_all_expenses')
    @login_required
    def get_all_expenses():
        expenses = expense_service.get_user_expenses(current_user.uid)
        data = [{
            'day_id': expense.day_id,
            'expense': expense.amount
        } for expense in expenses]

        return jsonify(data)
    
    # Route for setting budget
    @app.route('/set-budget', methods=['POST'])
    @login_required
    def set_budget():
        budget = float(request.form.get('set-budget'))
        if budget > 0:
            user_service.update_budget(current_user, budget, reset=True)
            
            notification_service.create_notification(
                user_id=current_user.uid,   
                title="New Budget Set",
                message=f"You have set your budget to be ${budget}."
            )

            expense_service.clear_expenses(current_user.uid)
        
            return jsonify({
                'budget': budget,
                'day': 1
            })
        
        return "Invalid budget", 400
    
    # Route for getting budget
    @app.route('/get-budget', methods=['GET'])
    @login_required
    def get_budget():
        return jsonify({'budget': current_user.budget})
    
    # Route for adding notification
    @app.route('/add-notification', methods=['POST'])
    @login_required
    def add_notification():
        data = request.get_json()

        # Extract title and message from the JSON payload
        title = data.get('title')
        message = data.get('message')

        # Validate the data
        if not title or not message:
            return jsonify({'message': 'Title and message are required'}), 400
        
        notification_service.create_notification(
            user_id=current_user.uid,
            title=title,
            message=message
        )

        return jsonify({'message': 'Notification added successfully'}), 201
    
    # Route for getting notifications
    @app.route('/get-notification', methods=['GET'])
    @login_required
    def get_notification():
        notifications = notification_service.get_user_notifications(current_user.uid)
        
        # If no notifications found
        if not notifications:
            return jsonify({'message': 'No notifications found'}), 404

        notifications_data = [{
            'id': notification.id,
            'title': notification.title,
            'message': notification.message,
            'created_at': notification.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for notification in notifications]

        return jsonify({'notifications': notifications_data}), 200