document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('loan-form');
    const calcBtn = document.getElementById('calc-btn');
    const resetBtn = document.getElementById('reset-btn');
    const loader = document.getElementById('loader');
    const btnText = document.querySelector('.btn-text');
    const errorMessage = document.getElementById('error-message');
    const resultsSection = document.getElementById('results-section');
    const scheduleSection = document.getElementById('schedule-section');
    const tbody = document.querySelector('#schedule-table tbody');

    // Format number as Indian Rupee (INR)
    const formatINR = (num) => {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(num);
    };

    // Helper to display errors
    const showError = (msg) => {
        errorMessage.textContent = msg;
        errorMessage.style.display = 'block';
        resultsSection.style.display = 'none';
        scheduleSection.style.display = 'none';
    };

    // Helper to hide errors
    const hideError = () => {
        errorMessage.style.display = 'none';
    };

    // Handle form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        hideError();

        // Get values
        const amount = parseFloat(document.getElementById('loan_amount').value);
        const rate = parseFloat(document.getElementById('interest_rate').value);
        const tenure = parseFloat(document.getElementById('tenure_years').value);

        // Client-side validation
        if (isNaN(amount) || amount <= 0) {
            showError("Loan amount must be greater than 0.");
            return;
        }
        if (isNaN(rate) || rate < 0) {
            showError("Interest rate cannot be negative.");
            return;
        }
        if (isNaN(tenure) || tenure <= 0) {
            showError("Tenure must be greater than 0.");
            return;
        }

        // Set UI to loading state
        btnText.textContent = 'Calculating...';
        loader.style.display = 'inline-block';
        calcBtn.disabled = true;

        try {
            // Call the FastAPI backend
            const response = await fetch('/api/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    loan_amount: amount,
                    interest_rate: rate,
                    tenure_years: tenure
                })
            });

            const data = await response.json();

            if (!response.ok) {
                // Check if validation error (422) or generic server error
                const errorDetail = data.messages ? data.messages.join(' | ') : (data.detail || 'Calculation failed');
                throw new Error(errorDetail);
            }

            // Populate Results Summary
            document.getElementById('res-emi').textContent = formatINR(data.emi);
            document.getElementById('res-interest').textContent = formatINR(data.total_interest);
            document.getElementById('res-total').textContent = formatINR(data.total_amount);

            // Populate Amortization Table
            tbody.innerHTML = ''; // Clear previous data
            data.schedule.forEach(item => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${item.month}</td>
                    <td>${formatINR(item.emi)}</td>
                    <td>${formatINR(item.principal)}</td>
                    <td>${formatINR(item.interest)}</td>
                    <td>${formatINR(item.balance)}</td>
                `;
                tbody.appendChild(tr);
            });

            // Make sections visible
            resultsSection.style.display = 'block';
            scheduleSection.style.display = 'block';

            // Smooth scroll down to results on mobile/desktop
            resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        } catch (err) {
            showError(err.message);
        } finally {
            // Restore button state
            btnText.textContent = 'Calculate';
            loader.style.display = 'none';
            calcBtn.disabled = false;
        }
    });

    // Handle form reset
    resetBtn.addEventListener('click', () => {
        hideError();
        resultsSection.style.display = 'none';
        scheduleSection.style.display = 'none';
        tbody.innerHTML = '';
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});
