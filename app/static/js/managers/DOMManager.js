class DOMManager {
    constructor() {
        // Initializes as null
        this.expenseForm = null;
        this.nextDayBtn = null;
        this.expenseList = null;
        this.expenseChart = null;
        this.budgetForm = null;
        this.budgetDisplay = null;
        this.dayDisplay = null;
    }

    initialize() {
        // Finds elements
        this.expenseForm = document.getElementById('add-expenses-form');
        this.nextDayBtn = document.getElementById('next-day-btn');
        this.expenseList = document.getElementById('expense-list');
        this.expenseChart = document.getElementById('expense-chart');
        this.budgetForm = document.getElementById('set-budget-form');
        this.budgetDisplay = document.getElementById('budget-display');
        this.dayDisplay = document.getElementById('current-day');

        // Adds event listeners if elements exist
        if (this.expenseForm) {
            this.expenseForm.addEventListener('submit', (e) => expenseManager.submitExpense(e));
        }
        if (this.nextDayBtn) {
            this.nextDayBtn.addEventListener('click', () => expenseManager.nextDay());
        }
        if (this.budgetForm) {
            this.budgetForm.addEventListener('submit', (e) => budgetManager.submitBudget(e));
        }
    }
    
    showMessage(message) {
        // Creates a message container
        let messageContainer = document.createElement('div');
        messageContainer.id = 'message-container';
        document.body.prepend(messageContainer);

        // Creates the div container
        const messageElement = document.createElement('div');
        messageElement.className = 'add-expense-message';
        messageElement.textContent = message;

        // Shows the message
        messageContainer.appendChild(messageElement);

        // Removes the message after 1 seconds
        setTimeout(() => {
            messageElement.remove();
            messageContainer.remove();
        }, 1000);
    }
}