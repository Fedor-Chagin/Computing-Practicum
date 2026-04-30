#!/usr/bin/env python3
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return f'GET request to: {request.path}\nAvailable: GET /api/data, POST /submit\n', 200, {'Content-Type': 'text/plain'}
    elif request.method == 'POST':
        return f'POST received\nURL: {request.path}\nData: {request.get_data(as_text=True)}\n', 200, {'Content-Type': 'text/plain'}

@app.route('/api/data', methods=['GET'])
def api_data():
    return f'{{"status":"ok","method":"GET","url":"{request.path}"}}\n', 200, {'Content-Type': 'application/json'}

@app.route('/submit', methods=['POST'])
def submit():
    return f'POST received\nURL: {request.path}\nData: {request.get_data(as_text=True)}\n', 200, {'Content-Type': 'text/plain'}

@app.errorhandler(405)
def method_not_allowed(e):
    return "Method not allowed\n", 405, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    print(f"Server on port 8888")
    print("\nTest commands:")
    print("  curl http://localhost:8888/")
    print("  curl http://localhost:8888/api/data")
    print("  curl -X POST -d \"message=apple.com\" http://localhost:8888/submit")
    print("\nPress Ctrl+C to stop\n")
    app.run(host='localhost', port=8888, debug=False)