from httpx import Response
from pydantic import BaseModel


def validate_status_code(response: Response, status_code: int):
    assert response.status_code == status_code, (
        f"Expected: {status_code}. Received: {response.status_code}. Details: {response.text}"
    )


def validate_model(response: Response, model: type[BaseModel]):
    model.model_validate(response.json())


def validate_contents(response: Response, contents: dict):
    assert contents.items() <= response.json().items(), (
        f"Expected: {contents}. Received: {response.json()}"
    )
