(function () {
  'use strict';
  
  const loginForm = document.getElementById('login-form');
  const payBillForm = document.getElementById('pay-bill-form');
  
  loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    fetch(`http://backend:8080/login?username=${username}&password=${password}`)
      .then((response) => response.text())
      .then((data) => {
        if (data === 'success') {
          // Show successful login message
          alert('Login successful!');
          // Hide login form and show pay bill form
          loginForm.style.display = 'none';
          payBillForm.style.display = 'block';
        } else {
          // Show error message
          alert('Invalid username or password');
        }
      })
      .catch((error) => {
        console.error(error);
      });
  });
  
  payBillForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const amount = document.getElementById('amount').value;
    const billType = document.getElementById('bill-type').value;
    
    fetch(`http://backend:8080/pay-bill?amount=${amount}&bill-type=${billType}`)
      .then((response) => response.text())
      .then((data) => {
        if (data === 'success') {
          // Show successful payment message
          alert('Bill payment completed successfully!');
        } else {
          // Show error message
          alert('Payment failed');
        }
      })
      .catch((error) => {
        console.error(error);
      });
  });
})();
```