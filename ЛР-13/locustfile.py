from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(0.5, 2)
    
    @task(1)
    def hello_world(self):
        self.client.get("/")
    
    @task(3)
    def slow_endpoint(self):
        self.client.get("/slow_endpoint")
    
    @task(2)
    def slow_endpoint_fixed(self):
        self.client.get("/slow_endpoint_fixed")
    
    @task(1)
    def high_cpu_endpoint(self):
        self.client.get("/high_cpu_endpoint")
    
    @task(1)
    def high_cpu_endpoint_fixed(self):
        self.client.get("/high_cpu_endpoint_fixed")
