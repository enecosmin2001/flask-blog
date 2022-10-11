import json
import unittest
from base64 import b64encode

from flask import url_for

from app import create_app, db
from app.models import Role, User


class APIV1TestCase(unittest.TestCase):
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

    def get_api_headers(self, username, password):
        return {
            "Authorization": "Basic "
            + b64encode((username + ":" + password).encode("utf-8")).decode("utf-8"),
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def test_no_auth(self):
        response = self.client.get(
            url_for("apiv1.get_posts"), content_type="application/json"
        )
        self.assertEqual(response.status_code, 401)

    def test_posts(self):
        r = Role.query.filter_by(name="User").first()
        self.assertIsNotNone(r)

        u = User(email="john@test.com", password="cat", confirmed=True, role=r)
        db.session.add(u)
        db.session.commit()

        # write a post
        response = self.client.post(
            url_for("apiv1.new_post"),
            headers=self.get_api_headers("john@test.com", "cat"),
            data=json.dumps({"body": "Body of the *blog* post"}),
        )

        self.assertEqual(response.status_code, 201)
        url = response.headers.get("Location")
        self.assertIsNotNone(url)

        # get the new post
        response = self.client.get(
            url, headers=self.get_api_headers("john@test.com", "cat")
        )

        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual("http://127.0.0.1:8943" + json_response["url"], url)
        self.assertEqual(json_response["body"], "Body of the *blog* post")
        self.assertEqual(
            json_response["body_html"], "<p>Body of the <em>blog</em> post</p>"
        )
