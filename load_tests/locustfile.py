from locust import HttpUser, task, between
import random
import os

def parse_test_data():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    test_file = os.path.join(base_dir, "data", "example.data")
    keys = []
    with open(test_file, encoding="utf-8") as file:
        for line in file:
            key, value = line.strip().split(" ", 1)
            keys.append(key)
    return keys

class KeyValueUser(HttpUser):
    wait_time = between(0.1, 1)
    keys = parse_test_data()

    @task
    def get_key(self):
        key = random.choice(self.keys)
        self.client.get(f"/key/{key}")
