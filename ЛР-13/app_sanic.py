from sanic import Sanic
from sanic.response import json
import asyncio
import time

app = Sanic("TestApp")

@app.route('/')
async def hello(request):
    return json({"Hello": "World"})

@app.route('/slow_endpoint')
async def slow_endpoint(request):
    await asyncio.sleep(0.1)  # НЕ БЛОКИРУЕТ!
    return json({"message": "Slow request (NON-BLOCKING!)"})

@app.route('/slow_endpoint_fixed')
async def slow_endpoint_fixed(request):
    await asyncio.sleep(0.1)
    return json({"message": "Slow request fixed (NON-BLOCKING!)"})

@app.route('/high_cpu_endpoint')
async def high_cpu_endpoint(request):
    def cpu_intensive():
        total = 0
        for i in range(1_000_000):
            total += i
        return total
    
    # БЛОКИРУЕТ!
    result = cpu_intensive()
    return json({"message": f"CPU result: {result} (BLOCKING!)"})

@app.route('/high_cpu_endpoint_fixed')
async def high_cpu_endpoint_fixed(request):
    def cpu_intensive():
        total = 0
        for i in range(1_000_000):
            total += i
        return total
    
    # НЕ БЛОКИРУЕТ!
    result = await asyncio.to_thread(cpu_intensive)
    return json({"message": f"CPU result: {result} (NON-BLOCKING!)"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, workers=4)