import re
import unittest

from app import create_app, db
from app.models import Role, User


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(response.headers.get("Location"))
        self.assertTrue("login" in response.headers.get("Location"))

    def test_register_and_login(self):
        # register a new account
        response = self.client.post(
            "/auth/register",
            data={
                "email": "cosmin@example.com",
                "username": "cosmin",
                "password": "test",
                "password2": "test",
            },
        )

        self.assertEqual(response.status_code, 302)

        # login with new account
        response = self.client.post(
            "/auth/login",
            data={"email": "cosmin@example.com", "password": "test"},
            follow_redirects=True,
        )

        self.assertTrue(response.status_code, 200)
        self.assertTrue(re.search(r"Hello,\s+cosmin!", response.get_data(as_text=True)))
        self.assertTrue(
            "You have not confirmed your account yet" in response.get_data(as_text=True)
        )

        # send a confirmation token
        user = User.query.filter_by(email="cosmin@example.com").first()
        token = user.generate_confirmation_token()
        response = self.client.get(f"/auth/confirm/{token}", follow_redirects=True)

        # user.confirm(token)
        self.assertTrue(response.status_code, 200)
        self.assertTrue(
            "You have confirmed your account" in response.get_data(as_text=True)
        )

        # log out
        response = self.client.get("/auth/logout", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("You have been logged out" in response.get_data(as_text=True))
