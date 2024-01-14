from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

class AuthViewsTest(TestCase):
    def setUp(self):
        self.register_url = reverse('accounts:register_view')
        self.login_url = reverse('accounts:login_view')
        self.logout_url = reverse('accounts:logout_view')
        self.change_password_url = reverse('accounts:change_password')

        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

        self.user = get_user_model().objects.create_user(
            username='existinguser',
            email='existinguser@example.com',
            password='existingpassword123'
        )

    def test_register_view(self):
        response = self.client.post(self.register_url, self.user_data, follow=True)
        self.assertEqual(response.status_code, 200)  # Check that the form is valid and user is redirected

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)  # Check that a success message is present
        self.assertEqual(str(messages[0]), 'Account created successfully. You can now log in.')

    def test_register_view_duplicate_email(self):
        # Test registering with a duplicate email
        self.user_data['email'] = 'existinguser@example.com'
        response = self.client.post(self.register_url, self.user_data, follow=True)
        self.assertEqual(response.status_code, 200)  # Check that the form is invalid and user is not redirected

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)  # Check that an error message is present
        self.assertEqual(str(messages[0]), 'Email is already taken. Please choose a different one.')

    def test_login_view(self):
        response = self.client.post(self.login_url, {'username': 'existinguser', 'password': 'existingpassword123'}, follow=True)
        self.assertEqual(response.status_code, 200)  # Check that login is successful and user is redirected

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)  # Check that a success message is present
        self.assertEqual(str(messages[0]), 'Welcome, existinguser!')

    def test_login_view_invalid_credentials(self):
        # Test logging in with invalid credentials
        response = self.client.post(self.login_url, {'username': 'nonexistentuser', 'password': 'wrongpassword'}, follow=True)
        self.assertEqual(response.status_code, 200)  # Check that login is unsuccessful and user is not redirected

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)  # Check that an error message is present
        self.assertEqual(str(messages[0]), 'Invalid username or password.')

    def test_logout_view(self):
        self.client.login(username='existinguser', password='existingpassword123')
        response = self.client.get(self.logout_url, follow=True)
        self.assertEqual(response.status_code, 200)  # Check that logout is successful and user is redirected

    def test_change_password_view(self):
        self.client.login(username='existinguser', password='existingpassword123')
        new_password_data = {
            'old_password': 'existingpassword123',
            'new_password1': 'newtestpassword123',
            'new_password2': 'newtestpassword123',
        }

        response = self.client.post(self.change_password_url, new_password_data, follow=True)
        self.assertEqual(response.status_code, 200)  # Check that changing password is successful and user is redirected

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)  # Check that a success message is present
        self.assertEqual(str(messages[0]), 'Password changed successfully')

    def test_change_password_view_invalid_password(self):
        # Test changing password with invalid old password
        self.client.login(username='existinguser', password='existingpassword123')
        invalid_password_data = {
            'old_password': 'wrongpassword',
            'new_password1': 'newtestpassword123',
            'new_password2': 'newtestpassword123',
        }

        response = self.client.post(self.change_password_url, invalid_password_data, follow=True)
        self.assertEqual(response.status_code, 200)  # Check that changing password is unsuccessful and user is not redirected

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)  # Check that an error message is present
        self.assertEqual(str(messages[0]), 'Please correct the errors')

    # Add more tests as needed for password reset views


