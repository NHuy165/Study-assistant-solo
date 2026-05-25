import requests
from locust import HttpUser, between, events, tag, task
from locust.exception import StopUser

from backend.src.core.config import settings
from load_test.common.auth import register_login


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


class AppUser(HttpUser):
    wait_time = between(1, 5)
    host = settings.BACKEND_URL

    def on_start(self):
        # Logins and saves token
        token = register_login(self.client)

        self.client.headers.update({"Authorization": f"Bearer {token}"})

        # Creates interaction
        response = self.client.post(
            "/api/interaction/create",
            json={
                "name": "interaction-name",
                "description": "interaction-description",
            },
        )

        if response.status_code != 200:
            raise StopUser()

        self.interaction_id = response.json()["id"]

    @tag("create_note")
    @task
    def create_note(self):
        self.client.post(
            f"/api/note/{self.interaction_id}/upload",
            json={
                "name": "note-name",
                "description": "note-description",
                "content": "note-content",
            },
            name="/api/note/{interaction_id}/upload",
        )

    @tag("create_llm_response")
    @task
    def create_llm_response(self):
        self.client.post(
            f"/api/llm-response/{self.interaction_id}/chat",
            json={"prompt": "Hãy giảng cho tôi về cách cộng trừ nhân chia phân số."},
            name="/api/llm-response/{interaction_id}/chat",
        )
        raise StopUser()
