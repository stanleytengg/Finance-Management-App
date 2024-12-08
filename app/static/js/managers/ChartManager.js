class ChartManager {
    constructor(domManager) {
        this.domManager = domManager;
    }

    sumTotals(dailyTotals, expense) {
        // Set total to 0 if it's first expense for the day
        if (!dailyTotals[expense.day_id]) dailyTotals[expense.day_id] = 0;
        // Add current expense to day's total
        dailyTotals[expense.day_id] += expense.expense;

        return dailyTotals;
    }

    async getDailyTotals() {
        // Get all expenses
        const expenses = await expenseManager.getAllExpenses();

        // Reduce expenses array into a dictionary of daily totals
        const dailyTotals = expenses.reduce(this.sumTotals, {});

        // Puts days as an array
        const days = Object.keys(dailyTotals);
        // Create array of corresponding total amounts
        const totals = days.map(day => dailyTotals[day]);

        return {days, totals};
    }

    async showChart() {
        if (!this.domManager.expenseChart) return;

        // Gets the canvas context for drawing the chart
        const chart = this.domManager.expenseChart.getContext('2d');
        const data = await this.getDailyTotals();

        // Create new Chart.js chart
        new Chart(chart, {
            type: 'line',
            data: {
                labels: data.days.map(day => `Day ${day}`),
                datasets: [{
                    label: 'Daily Total Expenses',
                    data: data.totals,
                    borderColor: '#5e503f',
                    backgroundColor: '#5e503f1a',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Daily Expenses Overview',
                        font: { size: 16 }
                    },
                    legend: { position: 'top' }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Amount ($)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Day'
                        }
                    }
                }
            }
        });
    }
}
