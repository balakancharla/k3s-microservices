(function () {
  'use strict';

  const loginForm = document.getElementById('login-form');
  const payBillForm = document.getElementById('pay-bill-form');

  // Hide pay bill form initially
  payBillForm.style.display = 'none';

  loginForm.addEventListener('submit', function (e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username, password })
    })
      .then(response => {
        if (!response.ok) throw new Error('Login failed');
        return response.json();
      })
      .then(data => {
        alert(data.message);

        // ✅ Show next section instead of reloading page
        loginForm.style.display = 'none';
        payBillForm.style.display = 'block';
      })
      .catch(() => {
        alert('Invalid username or password');
      });
  });

  payBillForm.addEventListener('submit', function (e) {
    e.preventDefault();

    const amount = document.getElementById('amount').value;
    const billType = document.getElementById('bill-type').value;

    fetch('/api/pay-bill', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ amount, billType })
    })
      .then(response => {
        if (!response.ok) throw new Error('Payment failed');
        return response.json();
      })
      .then(data => {
        alert(data.message);
      })
      .catch(() => {
        alert('Payment failed');
      });
  });
})();
