from fastapi import FastAPI
import asyncio
import time

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/slow_endpoint")
async def slow_endpoint():
    time.sleep(0.1)
    return {"message": "This was a slow request (BLOCKING!)"}

@app.get("/slow_endpoint_fixed")
async def slow_endpoint_fixed():
    await asyncio.sleep(0.1)
    return {"message": "This was a asyncio sleep (NON-BLOCKING!)"}

@app.get("/high_cpu_endpoint")
async def high_cpu_endpoint():
    def cpu_intensive_task():
        total = 0
        for i in range(10_000_000):
            total += i
        return total
    
    result = cpu_intensive_task()
    return {"message": f"CPU task completed with result: {result} (BLOCKING!)"}

@app.get("/high_cpu_endpoint_fixed")
async def high_cpu_endpoint_fixed():
    def cpu_intensive_task():
        total = 0
        for i in range(10_000_000):
            total += i
        return total
    
    result = await asyncio.to_thread(cpu_intensive_task)
    return {"message": f"CPU task completed with result: {result} (NON-BLOCKING!)"}
