// Initializes managers
const domManager = new DOMManager();
const expenseManager = new ExpenseManager(domManager);
const budgetManager = new BudgetManager(domManager);
const chartManager = new ChartManager(domManager);
const notificationManager = new NotificationManager(domManager);

// Set up the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', async function() {
    domManager.initialize();
    
    if (domManager.expenseList) {
        const expenses = await expenseManager.getAllExpenses();
        expenses.forEach(expense => expenseManager.updateExpenseList(expense));
    }
    
    if (domManager.expenseChart) {
        chartManager.showChart();
    }

    if (document.getElementById('budget-display')) {
        budgetManager.updateBudget();
    }

    if (document.getElementById('notification-list')) {
        notificationManager.updateNotifications();
    }
});