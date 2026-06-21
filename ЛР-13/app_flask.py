from flask import Flask, jsonify
import time
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=4)

@app.route('/')
def hello():
    return jsonify({"Hello": "World"})

@app.route('/slow_endpoint')
def slow_endpoint():
    time.sleep(0.1)
    return jsonify({"message": "Slow request (BLOCKING!)"})

@app.route('/slow_endpoint_fixed')
def slow_endpoint_fixed():
    time.sleep(0.1)
    return jsonify({"message": "Slow request (still BLOCKING in Flask!)"})

@app.route('/high_cpu_endpoint')
def high_cpu_endpoint():
    def cpu_intensive():
        total = 0
        for i in range(1_000_000):
            total += i
        return total
    
    result = cpu_intensive()
    return jsonify({"message": f"CPU result: {result} (BLOCKING!)"})

@app.route('/high_cpu_endpoint_fixed')
def high_cpu_endpoint_fixed():
    def cpu_intensive():
        total = 0
        for i in range(1_000_000):
            total += i
        return total
    
    future = executor.submit(cpu_intensive)
    result = future.result()
    return jsonify({"message": f"CPU result: {result} (in thread but still blocking!)"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, threaded=True, debug=False)