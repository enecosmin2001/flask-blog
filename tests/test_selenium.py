import re
import threading
import time
import unittest

from fake_useragent import UserAgent
from flask import url_for
from selenium import webdriver

import app.fake as fake
from app import create_app, db
from app.models import Role, User


class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls) -> None:
        options = webdriver.ChromeOptions()
        # options.add_argument("headless")
        # try:
        ua = UserAgent()
        user_agent = ua.random
        options.add_argument(f"user-agent={user_agent}")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        cls.client = webdriver.Chrome(chrome_options=options)
        # except:
        #     pass

        # skip these if the browser could not be started
        if cls.client:
            # create the app
            cls.app = create_app("testing")
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            # suppress logging to keep unittest output clean
            import logging

            logger = logging.getLogger("werkzeug")
            logger.setLevel("ERROR")

            # create db
            db.create_all()
            Role.insert_roles()
            fake.users(10)
            fake.posts(10)

            # add an administrator user
            admin_role = Role.query.filter_by(permissions=0xFF).first()
            admin = User(
                email="john@example.com",
                username="john",
                password="cat",
                role=admin_role,
                confirmed=True,
            )
            db.session.add(admin)
            db.session.commit()

            cls.server_thread = threading.Thread(
                target=cls.app.run,
                kwargs={
                    "host": "127.0.0.1",
                    "port": "8943",
                    "debug": "true",
                    "use_reloader": False,
                    "use_debugger": False,
                },
            )
            cls.server_thread.start()

    @classmethod
    def tearDownClass(cls) -> None:
        if cls.client:
            # stop the flask server
            cls.client.get("http://127.0.0.1:8943/shutdown")
            cls.client.quit()
            cls.server_thread.join()

            # destroy db
            db.session.remove()
            db.drop_all()

            # remove app context
            cls.app_context.pop()

    def setUp(self) -> None:
        if not self.client:
            self.skipTest("Web browser not available.")

    def tearDown(self) -> None:
        pass

    def test_admin_homepage(self):
        # navigate to home page
        self.client.get("http://127.0.0.1:8943/")
        self.assertTrue(
            re.search("Please log in to access this page", self.client.page_source)
        )
        # navigate to login page
        self.client.find_element("link text", "Log In").click()
        self.assertIn("<h1>Login</h1>", self.client.page_source)

        self.client.find_element("name", "email").send_keys("john@example.com")
        self.client.find_element("name", "password").send_keys("cat")
        self.client.find_element("name", "submit").click()
        self.assertTrue(re.search("Account", self.client.page_source))

        # navigate to the user's profile page
        self.client.find_element("link text", "Profile").click()
        self.assertIn("<h1>john</h1>", self.client.page_source)
