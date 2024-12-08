class ExpenseManager {
    constructor(domManager) {
        this.domManager = domManager;
    }

    async submitExpense(e) {
        e.preventDefault();
        
        // Loads expense amount into FormData object
        const expenseInput = document.getElementById('new-expense');
        const formData = new FormData();
        formData.append('add-expense', expenseInput.value);

        // Sends POST request and parse the response
        const response = await fetch('/add-expense', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();

        // Updates list and shows message if response and data is working
        if (response.ok && data) {
            this.updateExpenseList(data);
            this.domManager.showMessage('Expense added successfully!');
            budgetManager.updateBudget();
        }

        // Clears the input field
        expenseInput.value = '';
        
    }

    async nextDay() {
        // Sends POST request and parse the response
        const response = await fetch('/next-day', {
            method: 'POST'
        });
        const data = await response.json();

        // Update the day display if response and data is working
        if (response.ok && data) 
            this.domManager.dayDisplay.textContent = data.day;
    }

    async getAllExpenses() {
        // Sends GET request and parse the response
        const response = await fetch('/get_all_expenses', {
            method: 'GET'
        });
        const data = await response.json();

        return data;
    }

    updateExpenseList(data) {
        // Needs to return immediately if expense list doesn't exists
        if (!this.domManager.expenseList) return;

        // Add element in expense list
        const expenseElement = document.createElement('div');
        expenseElement.className = 'expense-item';
        expenseElement.innerHTML = `
            <span class="expense-day">Day ${data.day_id}</span>
            <span class="expense-amount">$${data.expense.toFixed(2)}</span>
        `;
        this.domManager.expenseList.prepend(expenseElement);
    }
}