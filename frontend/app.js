(function () {
  'use strict';

  const loginForm = document.getElementById('login-form');
  const payBillForm = document.getElementById('pay-bill-form');

  // Remove this line or wrap it:
  // payBillForm.style.display = 'none';

  if (loginForm) {
    loginForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const username = document.getElementById('username').value;
      const password = document.getElementById('password').value;

      fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      })
        .then(response => {
          if (!response.ok) throw new Error('Login failed');
          return response.json();
        })
        .then(data => {
          alert(data.message);
          window.location.href = 'pay-bill.html';  // redirect after login
        })
        .catch(() => alert('Invalid username or password'));
    });
  }

  if (payBillForm) {
    payBillForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const amount = document.getElementById('amount').value;
      const billType = document.getElementById('bill-type').value;

      fetch('/api/pay-bill', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ amount, billType })
      })
        .then(response => {
          if (!response.ok) throw new Error('Payment failed');
          return response.json();
        })
        .then(data => alert(data.message))
        .catch(() => alert('Payment failed'));
    });
  }
})();
