class BudgetManager {
    constructor(domManager) {
        this.domManager = domManager;
    }

    async submitBudget(e) {
        e.preventDefault();

        const budgetInput = document.getElementById('new-budget');
        const formData = new FormData();
        formData.append('set-budget', budgetInput.value);

        const response = await fetch('/set-budget', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();

        if (response.ok && data) {
            // Updates list and shows message if response and data is working
            this.updateBudget();

            // Clears expenses list
            if (this.domManager.expenseList) this.domManager.expenseList.innerHTML = '';
            
            // Updates day
            if (this.domManager.dayDisplay) this.domManager.dayDisplay.textContent = data.day;
        }

        // Clears the input field
        budgetInput.value = '';
    }

    updateBudget() {
        fetch('get-budget', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (!response.ok) {
                const budgetDisplay = document.getElementById('budget-display');
                if (budgetDisplay) {
                    budgetDisplay.innerText = `Budget: Not Set`;  // Update with the fetched budget value
                }
            }
            return response.json();  // Parse the JSON response
        })
        .then(data => {
            const budgetDisplay = document.getElementById('budget-display');
            if (budgetDisplay) {
                budgetDisplay.innerText = `Budget: $${data.budget.toFixed(2)}`;  // Update with the fetched budget value
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}