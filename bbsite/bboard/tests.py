"""Describe project test."""
from django.test import TestCase, Client
from django.contrib.auth.models import User

from bboard.models import Rubric

class TestSimple(TestCase):
    def test_str(self):
        self.assertEqual('abc', 'abc')


class TestRubric(TestCase):
    def test_str(self):
        r = Rubric()
        avto = 'Автомобили'
        r.name = avto
        self.assertEqual(str(r), avto)

    def test_create(self):
        count_rubric = Rubric.objects.count()
        r = Rubric.objects.create()
        r.name = 'Автомобили1'
        r.save()
        self.assertEqual(count_rubric + 1, Rubric.objects.count())

    def test_rubric_page(self):
        c = Client()
        response = c.get('/rubrics/')
        self.assertEqual(response.status_code, 200)


class TestLogin(TestCase):
    def setUp(self) -> None:
        self.credentials = {'username': 'user11', 'password': 'user11user11'}
        User.objects.create_user(**self.credentials)


    @staticmethod
    def make_request(credentials):
        return Client().post('/login/', credentials, follow=True)



    def test_login_bad_credentials(self):
        response = self.make_request({'username': 'user11', 'password': 'user11user1111'})
        self.assertFalse(response.context['user'].is_active)
        self.assertContains(
            response,
            'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.'
            )


    def test_login_success(self):
        response = self.make_request(self.credentials)
        self.assertTrue(response.context['user'].is_active)


    def test_login_empty_credentials(self):
        response = self.make_request({'username': '', 'password': ''})
        self.assertFalse(response.context['user'].is_active)
