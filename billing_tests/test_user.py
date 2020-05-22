from unittest import TestCase

from billing_tests.client import client


class UserTest(TestCase):
    """Check User api."""

    def test_user_create_redirect(self):
        """Expect proper redirect with trailing backslash on the end."""
        response = client.post("/users")
        assert response.status_code == 307
        assert response.headers == {"location": "http://testserver/users/"}

    def test_user_create_error(self):
        """Empty body should response 422 with details."""
        response = client.post("/users/")
        assert response.status_code == 422
        assert response.json() == {
            "detail": [
                {
                    "loc": ["body", "user"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }
