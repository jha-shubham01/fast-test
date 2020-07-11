import json

from django.contrib.auth.models import User
from django.urls import reverse

from fast.models import Post
from fast.serializers import PostSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class LoginTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Test@Password', email='test@localhost.com')
    def test_serializer(self):
        data = {'username':'testuser', 'password':'Test@Password'}
        response = self.client.post('/api/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PostTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(username='testuser', password='Test@Password', email='test@localhost.com')
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token "+self.token.key)

    def test_post_list_authenticated(self):
        response = self.client.get('/api/post/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_add_post_authenticated(self):
    #     data = {'post_title':'Post title', 'post_details':'This is post details'}
    #     response = self.client.post('/api/post/', data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ListPostTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='Test@Password', email='test@localhost.com')
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token "+self.token.key)

    def test_serializer(self):
        response = self.client.get('/api/list/post/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

