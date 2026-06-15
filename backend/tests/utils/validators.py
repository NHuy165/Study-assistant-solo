from typing import Any

from httpx import Response
from pydantic import BaseModel, TypeAdapter

# ----- STATUS CODE ----- #


def validate_status_code(response: Response, status_code: int) -> None:
    assert response.status_code == status_code, (
        f"Expected: {status_code}. Received: {response.status_code}. Details: {response.text}"
    )


# ----- MODEL ----- #


def validate_model(contents: dict, model: type[Any]) -> None:
    adapter = TypeAdapter(model)
    adapter.validate_python(contents)


def validate_response_model(response: Response, model: type[Any]) -> None:
    validate_model(response.json(), model)


# ----- CONTENTS ----- #


def is_subset_dict(received_contents: dict, expected_contents: dict) -> bool:
    for expected_key, expected_value in expected_contents.items():
        received_content = received_contents.get(expected_key)

        # If current value is a list
        if isinstance(expected_value, list):
            # If received content is None or not a list
            if received_content is None or not isinstance(received_content, list):
                return False
            # If content isn't the same
            elif not is_subset_list(received_content, expected_value):
                return False

        # If current value is a dict
        elif isinstance(expected_value, dict):
            # If received content is None or not a dict
            if received_content is None or not isinstance(received_content, dict):
                return False
            # If content isn't the same
            elif not is_subset_dict(received_content, expected_value):
                return False

        # If current value is a literal
        else:
            if received_content != expected_value:
                return False

    return True


def is_subset_list(received_contents: list, expected_contents: list) -> bool:
    """
    This function assumes what is being checked has no duplicated element.
    """
    for expected_content in expected_contents:
        # If current value is a dictionary
        if isinstance(expected_content, dict):
            for received_content in received_contents:
                if isinstance(received_content, dict) and is_subset_dict(
                    received_content, expected_content
                ):
                    break
            else:
                return False

        # If current value is a list
        elif isinstance(expected_content, list):
            for received_content in received_contents:
                if isinstance(received_content, list) and is_subset_list(
                    received_content, expected_content
                ):
                    break
            else:
                return False

        # if current value is a literal
        else:
            for received_content in received_contents:
                if expected_content == received_content:
                    break
            else:
                return False

    return True


def validate_contents_dict(received_contents: dict, expected_contents: dict) -> None:
    assert is_subset_dict(received_contents, expected_contents), (
        f"Expected: {expected_contents}. Received: {received_contents}"
    )


def validate_contents_list(received_contents: list, expected_contents: list) -> None:
    assert is_subset_list(received_contents, expected_contents), (
        f"Expected: {expected_contents}. Received: {received_contents}"
    )


def validate_object_contents(object: BaseModel, expected_contents: dict) -> None:
    validate_contents_dict(object.model_dump(), expected_contents)


def validate_response_contents(
    response: Response, expected_contents: dict | list[dict]
) -> None:
    response_contents = response.json()
    if isinstance(expected_contents, dict):
        assert isinstance(response_contents, dict), (
            "Response body can't be parsed into a dictionary."
        )
        validate_contents_dict(response_contents, expected_contents)

    else:
        assert isinstance(response_contents, list), (
            "Response body can't be parsed into a list."
        )
        validate_contents_list(response_contents, expected_contents)
