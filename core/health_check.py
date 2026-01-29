import requests

class HealthChecker:
    def __init__(self, name, url, circuit_breaker):
        self.name = name
        self.url = url
        self.circuit_breaker = circuit_breaker

    def check(self):
        try:
            r = requests.get(self.url, timeout=3)
            if r.status_code == 200:
                self.circuit_breaker.record_success()
        except:
            pass
