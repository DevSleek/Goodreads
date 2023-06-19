from django.contrib.auth import get_user
from .models import CustomUser
from django.test import TestCase
from django.urls import reverse


class RegistrationTestCase(TestCase):

    def test_user_account_is_created(self):
        self.client.post(
            reverse('users:register'), 
            data={
                'username': 'suhrob',
                'first_name': 'suhrob',
                'last_name': 'turaev',
                'email': 'suhrob@gmail.com',
                'password': "12345"
            }
        )

        user = CustomUser.objects.get(username='suhrob')

        self.assertEqual(user.first_name, 'suhrob')
        self.assertEqual(user.last_name, 'turaev')
        self.assertEqual(user.email, 'suhrob@gmail.com')
        self.assertNotEqual(user.password, "12345")
        self.assertTrue(user.check_password("12345"))

    def test_required_fields(self):
        response = self.client.post(
            reverse('users:register'), 
            data={
                'first_name': 'suhrob',
                'email': 'suhrob@gmail.com'
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'username', 'This field is required.')
        self.assertFormError(response, 'form', 'password', 'This field is required.')

    def test_invalid_email(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'suhrob',
                'first_name': 'suhrob',
                'last_name': 'turaev',
                'email': 'suhrobjkh',
                'password': "12345"
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_unique_username(self):
        user = CustomUser.objects.create(username='suhrob', first_name='suhrob')
        user.set_password("12345")
        user.save()

        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'suhrob',
                'first_name': 'suhrob',
                'last_name': 'turaev',
                'email': 'suhrob@gmail.com',
                'password': "12345"
            }
        )

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')


class LoginTestCase(TestCase):
    def setUp(self):
        self.user_db = CustomUser.objects.create(username='suhrob', first_name='suhrob')
        self.user_db.set_password("12345")
        self.user_db.save()

    def test_successful_login(self):
        self.client.post(
            reverse('users:login'),
            data={
                'username': 'suhrob',
                'password': "12345"
            }
        )
        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse('users:login'),
            data={
                'username': 'wrong-username',
                'password': "12345"
            }
        )

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse('users:login'),
            data={
                'username': 'suhrob',
                'password': "123456"
            }
        )

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        self.client.login(username='suhrob', password='12345')
        self.client.get(reverse('users:logout'))

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.url, reverse('users:login') + '?next=/users/profile/')

    def test_profile_detail(self):
        user = CustomUser.objects.create(username='sukhrob', first_name='Suhrob', last_name='Turaev', email='suhrobturaev2004@gmail.com')
        user.set_password('12345')
        user.save()

        self.client.login(username='sukhrob', password='12345')

        response = self.client.get(reverse('users:profile'))

        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_update_profile(self):
        user = CustomUser.objects.create(username='sukhrob', first_name='Suhrob', last_name='Turaev',
                                   email='suhrobturaev2004@gmail.com')
        user.set_password('12345')
        user.save()
        self.client.login(username='sukhrob', password='12345')

        response = self.client.post(
            reverse('users:profile-edit'),
            data={
                'username': 'Sukhrob',
                'first_name': 'Suhrob',
                'last_name': 'Turaev',
                'email': 'suhrobturaev200@gmail.com'
            }
        )
        user = CustomUser.objects.get(pk=user.pk)
        # OR user.refresh_from_db()

        self.assertEqual(user.username, 'Sukhrob')
        self.assertEqual(response.url, reverse('users:profile'))


