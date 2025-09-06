from typing import Dict

import pytest


@pytest.fixture
def user_data() -> Dict[str, str]:
    return {"username": "JohnDoe", "email": "john.doe@example.com", "password": "Password@123"}
