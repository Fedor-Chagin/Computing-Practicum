let monthlyBudget = 0;

function loadBudgetFromStorage() {
    const saved = localStorage.getItem('monthlyBudget');
    if (saved) {
        monthlyBudget = parseFloat(saved);
        const input = document.getElementById('monthlyBudgetInput');
        if (input) input.value = monthlyBudget;
        updateBudgetDisplay();
    }
}

function saveBudgetToStorage(budget) {
    localStorage.setItem('monthlyBudget', budget);
    monthlyBudget = budget;
    updateBudgetDisplay();
}

function getCurrencySymbol() {
    const symbols = { USD: '$', EUR: '€', RUB: '₽' };
    const currency = localStorage.getItem('currency') || 'USD';
    return symbols[currency] || '$';
}

function updateBudgetDisplay() {
    const budgetInput = document.getElementById('monthlyBudgetInput');
    const budget = parseFloat(budgetInput.value);
    
    if (isNaN(budget) || budget <= 0 || !window.Module) {
        document.getElementById('budgetDisplay').innerHTML = '<p style="color: #666;">No budget set. Enter amount and click Set Budget.</p>';
        return;
    }
    
    const spent = window.Module._jsGetTotalExpenses();
    const remaining = budget - spent;
    const percentage = Math.min((spent / budget) * 100, 100);
    const symbol = getCurrencySymbol();
    
    let fillColor = '#4CAF50';
    if (percentage > 90) fillColor = '#f44336';
    else if (percentage > 70) fillColor = '#ff9800';
    
    document.getElementById('budgetDisplay').innerHTML = `
        <div style="display: flex; justify-content: space-between; margin-top: 10px; flex-wrap: wrap; gap: 10px;">
            <div><strong>Budget:</strong> ${symbol}${budget.toFixed(2)}</div>
            <div><strong>Spent:</strong> ${symbol}${spent.toFixed(2)}</div>
            <div><strong>Remaining:</strong> <span style="color: ${remaining < 0 ? '#f44336' : '#4CAF50'};">${symbol}${remaining.toFixed(2)}</span></div>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" style="width: ${percentage}%; background: ${fillColor};">
                ${percentage.toFixed(0)}%
            </div>
        </div>
        ${remaining < 0 ? `<div style="color: #f44336; margin-top: 10px;">Over budget by ${symbol}${Math.abs(remaining).toFixed(2)}</div>` : 
          percentage > 90 ? `<div style="color: #ff9800; margin-top: 10px;">Warning: Only ${symbol}${remaining.toFixed(2)} left</div>` : ''}
    `;
}

document.addEventListener('DOMContentLoaded', function() {
    const setBtn = document.getElementById('setBudgetBtn');
    const resetBtn = document.getElementById('resetBudgetBtn');
    const input = document.getElementById('monthlyBudgetInput');
    
    if (setBtn) {
        setBtn.addEventListener('click', function() {
            const budget = parseFloat(input.value);
            if (!isNaN(budget) && budget > 0) {
                saveBudgetToStorage(budget);
                alert('Budget set to ' + getCurrencySymbol() + budget.toFixed(2));
            } else {
                alert('Please enter a valid budget amount');
            }
        });
    }
    
    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            if (confirm('Reset monthly budget?')) {
                localStorage.removeItem('monthlyBudget');
                monthlyBudget = 0;
                if (input) input.value = '';
                updateBudgetDisplay();
                alert('Budget reset');
            }
        });
    }
    
    loadBudgetFromStorage();
    
    // Hook into update functions
    const origUpdateTotal = window.updateTotalExpenses;
    if (origUpdateTotal) {
        window.updateTotalExpenses = function(total) {
            origUpdateTotal(total);
            updateBudgetDisplay();
        };
    }
    
    const origUpdateTable = window.updateExpenseTable;
    if (origUpdateTable) {
        window.updateExpenseTable = function() {
            origUpdateTable();
            updateBudgetDisplay();
        };
    }
});
