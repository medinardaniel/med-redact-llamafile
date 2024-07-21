import pytest
import json
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class MockChoice:
    def __init__(self, content):
        self.message = MockMessage(content)


class MockMessage:
    def __init__(self, content):
        self.content = content


class MockResponse:
    def __init__(self, choices):
        self.choices = choices


def test_redact_success(client, mocker):
    mockres = MockResponse(
        [
            MockChoice(
                "Hi my name is <REDACTED> and I really need my medication "
                "shipped to <REDACTED>. You can also reach me at <REDACTED> "
                "or at <REDACTED>."
            )
        ]
    )

    mocker.patch("app.client.chat.completions.create", return_value=mockres)

    response = client.post(
        "/redact",
        data=json.dumps(
            {
                "text": "Hi my name is Josephine Smith and I really need my "
                "medication shipped to Gotham, NJ 07030. You can also reach "
                "me at 123-565-1222 or at jsmith@gmail.com."
            }
        ),
        content_type="application/json",
    )

    data = json.loads(response.data)
    assert response.status_code == 200
    assert "redacted_text" in data
    assert (
        data["redacted_text"]
        == "Hi my name is <REDACTED> and I really need my medication shipped "
        "to <REDACTED>. You can also reach me at <REDACTED> or at <REDACTED>."
    )


def test_redact_no_text(client):
    response = client.post(
        "/redact", data=json.dumps({}), content_type="application/json"
    )
    data = json.loads(response.data)
    assert response.status_code == 400
    assert "error" in data
    assert data["error"] == "No text provided"


def test_redact_invalid_json(client):
    response = client.post(
        "/redact", data="Invalid JSON", content_type="application/json"
    )
    assert response.status_code == 400
