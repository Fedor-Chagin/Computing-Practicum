document.addEventListener('DOMContentLoaded', function() {
    const expenseForm = document.getElementById('expenseForm');
    const expenseDate = document.getElementById('expenseDate');
    const expenseCategory = document.getElementById('expenseCategory');
    const expenseAmount = document.getElementById('expenseAmount');
    const expenseDescription = document.getElementById('expenseDescription');
    const clearAllBtn = document.getElementById('clearAllBtn');
    const expenseTableBody = document.getElementById('expenseTableBody');
    const noExpensesRow = document.getElementById('noExpensesRow');
    const totalExpensesElement = document.getElementById('totalExpenses');
    const categoryTotalsElement = document.getElementById('categoryTotals');
    const noCategoriesMessage = document.getElementById('noCategoriesMessage');
    const messageArea = document.getElementById('messageArea');
    
    expenseDate.value = new Date().toISOString().substr(0, 10);
    
    // ========== CURRENCY FEATURE ==========
    let currentCurrency = 'USD';
    let currencySymbol = '$';
    let exchangeRates = { USD: 1, EUR: 0.92, RUB: 91.5 };
    
    async function fetchExchangeRates() {
        const apis = [
            'https://api.exchangerate-api.com/v4/latest/USD',
            'https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/usd.json'
        ];
        
        for (const api of apis) {
            try {
                const response = await fetch(api);
                if (response.ok) {
                    const data = await response.json();
                    if (data.rates) {
                        exchangeRates = { USD: 1, EUR: data.rates.EUR || 0.92, RUB: data.rates.RUB || 91.5 };
                    } else if (data.usd) {
                        exchangeRates = { USD: 1, EUR: data.usd.eur || 0.92, RUB: data.usd.rub || 91.5 };
                    }
                    refreshCurrencyDisplay();
                    return;
                }
            } catch (error) {}
        }
    }
    
    function loadCurrency() {
        const saved = localStorage.getItem('currency');
        if (saved) {
            currentCurrency = saved;
            const select = document.getElementById('currencySelect');
            if (select) select.value = currentCurrency;
            updateCurrencySymbol();
        }
    }
    
    function updateCurrencySymbol() {
        const symbols = { USD: '$', EUR: '€', RUB: '₽' };
        currencySymbol = symbols[currentCurrency] || '$';
        const symbolSpan = document.getElementById('currencySymbol');
        if (symbolSpan) symbolSpan.textContent = currencySymbol;
        refreshCurrencyDisplay();
    }
    
    function convertAmount(amountUSD) {
        return amountUSD * exchangeRates[currentCurrency];
    }
    
    function formatCurrency(amountUSD) {
        return currencySymbol + convertAmount(amountUSD).toFixed(2);
    }
    
    function refreshCurrencyDisplay() {
        if (window.Module) {
            totalExpensesElement.textContent = formatCurrency(window.Module._jsGetTotalExpenses());
            window.updateExpenseTable();
            window.updateCategoryTotals();
            window.updateBudgetDisplay();
        }
    }
    
    const currencySelect = document.getElementById('currencySelect');
    if (currencySelect) {
        currencySelect.addEventListener('change', function() {
            currentCurrency = this.value;
            localStorage.setItem('currency', currentCurrency);
            updateCurrencySymbol();
        });
    }
    
    const refreshBtn = document.getElementById('refreshRatesBtn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', () => fetchExchangeRates());
    }
    // ========== END CURRENCY FEATURE ==========
    
    function showMessage(message, type) {
        messageArea.textContent = message;
        messageArea.className = type === 'error' ? 'error-message' : 'success-message';
        messageArea.classList.remove('hidden');
        setTimeout(() => messageArea.classList.add('hidden'), 3000);
    }
    
    function handleAddExpense(event) {
        event.preventDefault();
        
        const date = expenseDate.value;
        const category = expenseCategory.value;
        const amountStr = expenseAmount.value;
        const description = expenseDescription.value;
        
        if (!date || !category || !amountStr || !description) {
            showMessage('Please fill in all fields', 'error');
            return;
        }
        
        const amount = parseFloat(amountStr);
        if (isNaN(amount) || amount <= 0) {
            showMessage('Please enter a valid positive amount', 'error');
            return;
        }
        
        const datePtr = Module._malloc(date.length + 1);
        const categoryPtr = Module._malloc(category.length + 1);
        const descriptionPtr = Module._malloc(description.length + 1);
        
        Module.stringToUTF8(date, datePtr, date.length + 1);
        Module.stringToUTF8(category, categoryPtr, category.length + 1);
        Module.stringToUTF8(description, descriptionPtr, description.length + 1);
        
        const result = Module._jsAddExpense(datePtr, categoryPtr, amount, descriptionPtr);
        
        Module._free(datePtr);
        Module._free(categoryPtr);
        Module._free(descriptionPtr);
        
        if (result === 1) {
            showMessage('Expense added successfully', 'success');
            expenseCategory.value = '';
            expenseAmount.value = '';
            expenseDescription.value = '';
            expenseCategory.focus();
            refreshCurrencyDisplay();
        } else {
            showMessage('Failed to add expense. Maximum number of expenses reached.', 'error');
        }
    }
    
    function handleDeleteExpense(index) {
        if (Module._jsDeleteExpense(index) === 1) {
            showMessage('Expense deleted successfully', 'success');
            refreshCurrencyDisplay();
        } else {
            showMessage('Failed to delete expense. Invalid index.', 'error');
        }
    }
    
    function handleClearAllExpenses() {
        if (confirm('Are you sure you want to clear all expenses?')) {
            if (Module._jsClearAllExpenses() === 1) {
                showMessage('All expenses cleared successfully', 'success');
                refreshCurrencyDisplay();
            } else {
                showMessage('Failed to clear expenses', 'error');
            }
        }
    }
    
    window.updateExpenseTable = function() {
        const expenseCount = Module._jsGetExpenseCount();
        expenseTableBody.innerHTML = '';
        
        if (expenseCount === 0) {
            expenseTableBody.appendChild(noExpensesRow);
            return;
        }
        
        for (let i = 0; i < expenseCount; i++) {
            const expenseJsonPtr = Module._getExpenseJSON(i);
            if (expenseJsonPtr === 0) continue;
            
            const expense = JSON.parse(Module.UTF8ToString(expenseJsonPtr));
            Module._freeMemory(expenseJsonPtr);
            
            const row = document.createElement('tr');
            row.insertCell(0).textContent = expense.date;
            row.insertCell(1).textContent = expense.category;
            row.insertCell(2).textContent = formatCurrency(expense.amount);
            row.insertCell(3).textContent = expense.description;
            
            const deleteBtn = document.createElement('button');
            deleteBtn.textContent = 'Delete';
            deleteBtn.className = 'delete';
            deleteBtn.onclick = (function(idx) { return () => handleDeleteExpense(idx); })(i);
            row.insertCell(4).appendChild(deleteBtn);
            
            expenseTableBody.appendChild(row);
        }
    };
    
    window.updateTotalExpenses = function(totalUSD) {
        totalExpensesElement.textContent = formatCurrency(totalUSD);
    };
    
    window.updateCategoryTotals = function() {
        const categoryCount = Module._jsGetCategoryCount();
        categoryTotalsElement.innerHTML = '';
        
        if (categoryCount === 0) {
            categoryTotalsElement.appendChild(noCategoriesMessage);
            return;
        }
        
        for (let i = 0; i < categoryCount; i++) {
            const categoryJsonPtr = Module._getCategoryTotalJSON(i);
            if (categoryJsonPtr === 0) continue;
            
            const category = JSON.parse(Module.UTF8ToString(categoryJsonPtr));
            Module._freeMemory(categoryJsonPtr);
            
            const categoryElement = document.createElement('div');
            categoryElement.className = 'category-total-item';
            categoryElement.textContent = `${category.name}: ${formatCurrency(category.total)}`;
            categoryTotalsElement.appendChild(categoryElement);
        }
    };
    
    window.updateBudgetDisplay = function() {
        const budgetInput = document.getElementById('monthlyBudgetInput');
        const budgetUSD = parseFloat(budgetInput.value);
        
        if (isNaN(budgetUSD) || budgetUSD <= 0 || !window.Module) {
            const budgetDisplay = document.getElementById('budgetDisplay');
            if (budgetDisplay) {
                budgetDisplay.innerHTML = '<p style="color: #666;">No budget set. Enter amount and click Set Budget.</p>';
            }
            return;
        }
        
        const spentUSD = window.Module._jsGetTotalExpenses();
        const rate = exchangeRates[currentCurrency];
        const budget = budgetUSD * rate;
        const spent = spentUSD * rate;
        const remaining = budget - spent;
        const percentage = Math.min((spent / budget) * 100, 100);
        
        let fillColor = '#4CAF50';
        if (percentage > 90) fillColor = '#f44336';
        else if (percentage > 70) fillColor = '#ff9800';
        
        const budgetDisplay = document.getElementById('budgetDisplay');
        if (budgetDisplay) {
            budgetDisplay.innerHTML = `
                <div class="budget-stats">
                    <div class="budget-stat"><strong>Budget:</strong><br>${currencySymbol}${budget.toFixed(2)}</div>
                    <div class="budget-stat"><strong>Spent:</strong><br>${currencySymbol}${spent.toFixed(2)}</div>
                    <div class="budget-stat"><strong>Remaining:</strong><br><span style="color:${remaining<0?'#f44336':'#4CAF50'}">${currencySymbol}${remaining.toFixed(2)}</span></div>
                </div>
                <div class="progress-bar"><div class="progress-fill" style="width:${percentage}%;background:${fillColor}">${percentage.toFixed(0)}%</div></div>
                ${remaining<0?`<div style="color:#f44336;text-align:center">Over budget by ${currencySymbol}${Math.abs(remaining).toFixed(2)}</div>`:percentage>90?`<div style="color:#ff9800;text-align:center">Warning: Only ${currencySymbol}${remaining.toFixed(2)} left</div>`:''}
            `;
        }
    };
    
    expenseForm.addEventListener('submit', handleAddExpense);
    clearAllBtn.addEventListener('click', handleClearAllExpenses);
    
    loadCurrency();
    fetchExchangeRates();
    setInterval(fetchExchangeRates, 300000);
});
