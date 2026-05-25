import requests
from locust import events

from backend.src.core.config import settings


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    try:
        response = requests.post(f"{settings.BACKEND_URL}/api/dev/wipe-db")

        if response.status_code == 200:
            print("Database wiped. Tests are starting.")
        else:
            print(f"Failed to wipe database. Status code: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("Failed to connect to the server.")
        environment.runner.quit()
