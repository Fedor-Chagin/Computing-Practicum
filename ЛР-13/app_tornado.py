import tornado.ioloop
import tornado.web
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=4)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write({"Hello": "World"})

class SlowHandler(tornado.web.RequestHandler):
    async def get(self):
        await asyncio.sleep(0.1)  # НЕ БЛОКИРУЕТ!
        self.write({"message": "Slow request (NON-BLOCKING!)"})

class SlowHandlerFixed(tornado.web.RequestHandler):
    async def get(self):
        await asyncio.sleep(0.1)
        self.write({"message": "Slow request fixed (NON-BLOCKING!)"})

class CPUHandler(tornado.web.RequestHandler):
    async def get(self):
        def cpu_intensive():
            total = 0
            for i in range(1_000_000):
                total += i
            return total
        
        # БЛОКИРУЕТ, если запустить напрямую!
        result = cpu_intensive()
        self.write({"message": f"CPU result: {result} (BLOCKING!)"})

class CPUHandlerFixed(tornado.web.RequestHandler):
    async def get(self):
        def cpu_intensive():
            total = 0
            for i in range(1_000_000):
                total += i
            return total
        
        # НЕ БЛОКИРУЕТ - в отдельном потоке!
        result = await tornado.ioloop.IOLoop.current().run_in_executor(executor, cpu_intensive)
        self.write({"message": f"CPU result: {result} (NON-BLOCKING!)"})

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/slow_endpoint", SlowHandler),
        (r"/slow_endpoint_fixed", SlowHandlerFixed),
        (r"/high_cpu_endpoint", CPUHandler),
        (r"/high_cpu_endpoint_fixed", CPUHandlerFixed),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Tornado running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()