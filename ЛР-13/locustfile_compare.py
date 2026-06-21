from locust import HttpUser, task, between

class FastAPIUser(HttpUser):
    wait_time = between(0.5, 2)
    host = "http://127.0.0.1:8000"
    
    @task(2)
    def high_cpu(self):
        self.client.get("/high_cpu_endpoint")
    
    @task(2)
    def high_cpu_fixed(self):
        self.client.get("/high_cpu_endpoint_fixed")

class FlaskUser(HttpUser):
    wait_time = between(0.5, 2)
    host = "http://127.0.0.1:5000"
    
    @task(2)
    def high_cpu(self):
        self.client.get("/high_cpu_endpoint")
    
    @task(2)
    def high_cpu_fixed(self):
        self.client.get("/high_cpu_endpoint_fixed")

class TornadoUser(HttpUser):
    wait_time = between(0.5, 2)
    host = "http://127.0.0.1:8888"
    
    @task(2)
    def high_cpu(self):
        self.client.get("/high_cpu_endpoint")
    
    @task(2)
    def high_cpu_fixed(self):
        self.client.get("/high_cpu_endpoint_fixed")

class SanicUser(HttpUser):
    wait_time = between(0.5, 2)
    host = "http://127.0.0.1:8001"
    
    @task(2)
    def high_cpu(self):
        self.client.get("/high_cpu_endpoint")
    
    @task(2)
    def high_cpu_fixed(self):
        self.client.get("/high_cpu_endpoint_fixed")