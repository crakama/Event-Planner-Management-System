# tests.py
import os
import unittest

from flask_testing import TestCase
from flask import abort, user_for
from app import create_app, db
from app.models import RemoteUser, Role, Event

class TestBase(TestCase):

    def create_app(self):

        # pass in test configurations
        config_name = 'testing'
        app = create_app(config_name)
        app.config.update(
            SQLALCHEMY_DATABASE_URI='mysql://kth_admin:kth2017@localhost/kth_test'
        )
        return app

    def setUp(self):
        """
        Will be called before every test
        """

        db.create_all()

        # create test admin user
        admin = RemoteUser(username="admin", password="admin2017", is_admin=True)

        # create test non-admin user
        remoteuser = RemoteUser(username="test_user", password="test2017")

        # save users to database
        db.session.add(admin)
        db.session.add(remoteuser)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()

class TestModels(TestBase):

    def test_remoteuser_model(self):
        """
        Test number of records in RemoteUser table
        """
        self.assertEqual(RemoteUser.query.count(), 2)

    def test_event_model(self):
        """
        Test number of records in Event table
        """
        # create test event
        event = Event(name="Wedding", description="The Wedding Event")

        # save event to database
        db.session.add(event)
        db.session.commit()

        self.assertEqual(Event.query.count(), 1)

    def test_role_model(self):
        """
        Test if you can add data to DB by inserting a temporary value then
        count the number of records in Role table to confirm insert works
        """

        # create test role
        role = Role(name="CEO", description="Run the whole company")

        # save role to database
        db.session.add(role)
        db.session.commit()

        self.assertEqual(Role.query.count(), 1)

class TestViews(TestBase):

    def test_homepage_view(self):
        """
        Test that homepage is accessible without login
        """
        response = self.client.get(url_for('home.homepage '))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        """
        Test that login page is accessible without login
        """
        response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        """
        Test that logout link is inaccessible without login
        and redirects to login page then to logout
        """
        target_url = url_for('auth.logout')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_dashboard_view(self):
        """
        Test that dashboard is inaccessible without login
        and redirects to login page then to dashboard
        """
        target_url = url_for('home.dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_admin_dashboard_view(self):
        """
        Test that dashboard is inaccessible without login
        and redirects to login page then to dashboard
        """
        target_url = url_for('home.admin_dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_events_view(self):
        """
        Test that events page is inaccessible without login
        and redirects to login page then to events page
        """
        target_url = url_for('admin.list_events')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_roles_view(self):
        """
        Test that roles page is inaccessible without login
        and redirects to login page then to roles page
        """
        target_url = url_for('admin.list_roles')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_remoteuser_view(self):
        """
        Test that users page is inaccessible without login
        and redirects to login page then to users page
        """
        target_url = url_for('admin.list_remoteusers')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

class TestErrorPages(TestBase):

    def test_403_forbidden(self):
        # create route to abort the request with the 403 Error
        @self.app.route('/403')
        def forbidden_error():
            abort(403)

        response = self.client.get('/403')
        self.assertEqual(response.status_code, 403)
        self.assertTrue("403 Error" in response.data)

    def test_404_not_found(self):
        response = self.client.get('/nothinghere')
        self.assertEqual(response.status_code, 404)
        self.assertTrue("404 Error" in response.data)

    def test_500_internal_server_error(self):
        # create route to abort the request with the 500 Error
        @self.app.route('/500')
        def internal_server_error():
            abort(500)

        response = self.client.get('/500')
        self.assertEqual(response.status_code, 500)
        self.assertTrue("500 Error" in response.data)


if __name__ == '__main__':
    unittest.main()
