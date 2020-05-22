import logging
from unittest import TestCase

from billing import models
from billing.database import get_db
from billing_tests.client import client

# for more transparency enable sql logs for this test
logging.basicConfig()
logger = logging.getLogger("sqlalchemy.engine")
logger.setLevel(logging.DEBUG)


class PaymentTest(TestCase):
    """Check User api."""

    TEST_EMAIL_1 = "john1@example.org"
    TEST_EMAIL_2 = "john2@example.org"

    def setUp(self):
        """Setup db connection, register cleanup."""
        super().setUp()
        self.db = next(get_db())  # not sure if that is correct way to get db in tests
        self.addCleanup(self.cleanup_models)

    def cleanup_models(self):
        """Delete test Users."""
        self.db.query(models.Payment).delete()
        self.db.query(models.User).delete()
        self.db.commit()

    def test_user_create_0(self):
        """Create user with proper params."""
        self.assertEqual(self.db.query(models.User).count(), 0)
        self.assertEqual(self.db.query(models.Payment).count(), 0)
        response = client.post(
            "/users/",
            json={
                "username": "jsmith",
                "balance": 0,
                "email": self.TEST_EMAIL_1,
                "full_name": "John Smith",
                "password": "secure_text_here",
            },
        )
        assert response.status_code == 200
        assert response.json() == {
            "username": "jsmith",
            "balance": 0,
            "email": self.TEST_EMAIL_1,
            "full_name": "John Smith",
        }
        self.assertEqual(self.db.query(models.User).count(), 1)
        self.assertEqual(self.db.query(models.User).first().balance, 0)
        self.assertEqual(self.db.query(models.Payment).count(), 1)
        self.assertEqual(self.db.query(models.Payment).first().amount, 0)

    def test_user_payment(self):
        """Create user with proper params."""
        # create first user
        self.assertEqual(self.db.query(models.User).count(), 0)
        self.assertEqual(self.db.query(models.Payment).count(), 0)
        response = client.post(
            "/users/",
            json={
                "username": "jsmith",
                "balance": 53,
                "email": self.TEST_EMAIL_1,
                "full_name": "John Smith",
                "password": "secure_text_here",
            },
        )
        assert response.status_code == 200
        assert response.json() == {
            "username": "jsmith",
            "balance": 53,
            "email": self.TEST_EMAIL_1,
            "full_name": "John Smith",
        }
        self.assertEqual(self.db.query(models.User).count(), 1)
        self.assertEqual(self.db.query(models.User).first().balance, 53)
        self.assertEqual(self.db.query(models.Payment).count(), 1)
        self.assertEqual(self.db.query(models.Payment).first().amount, 53)

        # create second user
        response = client.post(
            "/users/",
            json={
                "username": "jsmith2",
                "balance": 7,
                "email": self.TEST_EMAIL_2,
                "full_name": "John2 Smith",
                "password": "secure_text_here",
            },
        )
        assert response.status_code == 200
        assert response.json() == {
            "username": "jsmith2",
            "balance": 7,
            "email": self.TEST_EMAIL_2,
            "full_name": "John2 Smith",
        }
        self.assertEqual(self.db.query(models.User).count(), 2)
        self.assertEqual(self.db.query(models.Payment).count(), 2)
        users = self.db.query(models.User)
        payments = self.db.query(models.Payment)
        self.assertEqual(users[1].balance, 7)
        self.assertEqual(payments[1].amount, 7)

        # crate correct payment
        response = client.post(
            "/payments/",
            json={"debit_id": users[0].id, "credit_id": users[1].id, "amount": 2},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"debit_id": users[0].id, "credit_id": users[1].id, "amount": 2},
        )
        self.assertEqual(self.db.query(models.Payment).count(), 3)
        payments = self.db.query(models.Payment)
        last_payment_id = payments[2].id
        self.db.refresh(users[0])
        self.db.refresh(users[1])
        self.assertEqual(users[0].last_payment_id, last_payment_id)
        self.assertEqual(users[1].last_payment_id, last_payment_id)
        self.assertEqual(users[0].balance, 55)  # 53+2=55
        self.assertEqual(users[1].balance, 5)  # 7-2=5

        # crate wrong payment
        response = client.post(
            "/payments/",
            json={"debit_id": users[0].id, "credit_id": users[1].id, "amount": 6},
        )
        self.assertEqual(response.status_code, 406)
        self.assertEqual(
            response.json(), {"detail": "not enough founds"},
        )
        self.assertEqual(self.db.query(models.Payment).count(), 3)
