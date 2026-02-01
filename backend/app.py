```
from flask import Flask, request, jsonify
import json

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_TRUE"] = False
app.run(port=8080)

@app.route('/api/login', methods=['POST'])
def login():
    data = json.loads(request.data)
    if data.get('username') == 'admin' and data.get('password') == 'password':
        return jsonify({'message': 'Logged in successfully'})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/pay-bill', methods=['POST'])
def pay_bill():
    return jsonify({'message': 'Bill paid successfully'})

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'UP'})
```