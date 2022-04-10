from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Post, Comment
from rest_framework.settings import api_settings

class RegistrationTestCase(APITestCase):

    def test_valid_data(self):
        data = {'username': 'test_user', 'password': 'strong_1234', 'repeat_password': 'strong_1234'}
        response = self.client.post('/api/auth/register/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            'Status 201 if register data is valid')
        self.assertEqual(response.data, {'username': 'test_user'}, 
            'API should return username only')
        self.assertTrue(User.objects.filter(username='test_user').exists(), 
            'User should be created in DB')

    def test_passwords_dont_match(self):
        data = {'username': 'passwords_dont_match', 'password': 'strong_1234', 'repeat_password': 'not_matches'}
        response = self.client.post('/api/auth/register/', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            "Status 400 if passwords don't match")
        self.assertFalse(User.objects.filter(username='passwords_dont_match').exists(), 
            'User should not be created in DB')

    def test_bad_username(self):
        data = {'username': '111111', 'password': 'strong_1234', 'repeat_password': 'strong_1234'}
        response = self.client.post('/api/auth/register/', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            'Status 400 if username is numeric')
        self.assertFalse(User.objects.filter(username='111111').exists(), 
            'User should not be created in DB')

class AuthTestCase(APITestCase):
    username = 'test_user'
    password = 'strong_pass'

    def setUp(self):
        user = User.objects.create(username=self.username)
        user.set_password(self.password)
        user.save()

    def test_existing_user_can_authorize(self):
        data = {'username': self.username, 'password': self.password}
        response = self.client.post('/api/auth/login/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK, 
            'Status 200 if data is correct')
        self.assertIsNotNone(response.data['token'], 
            'Should return token')

    def test_not_existing_user_cannot_authorize(self):
        data = {'username': 'not_exists', 'password': '12345678'}
        response = self.client.post('/api/auth/login/', data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 
            'Status 400 if data is not correct')

class PostsTestCase(APITestCase):
    username = 'test_user'
    password = 'strong_pass'
    user = None
    token = None
    post_count = 22

    def setUp(self):
        self.user = User.objects.create(username=self.username)
        self.user.set_password(self.password)
        self.user.save()

        for i in range(self.post_count):
            post = Post.objects.create(title=f'title {i}', body=f'body {i}', author=self.user)
            post.save()

        # get token before creating posts
        response = self.client.post('/api/auth/login/', data={'username': self.username, 'password': self.password})
        self.token = response.data['token']

    def test_get_all_posts_without_query_params(self):
        response = self.client.get('/api/posts/')

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            'Status 200 for get all posts')
        self.assertEqual(response.data['count'], self.post_count, 
            f'Posts total count should be as generated {self.post_count}')
        self.assertEqual(len(response.data['results']), api_settings.PAGE_SIZE,
            f'Posts actual count should be as defined in PAGE_SIZE={api_settings.PAGE_SIZE}')

    def test_get_all_posts_limit10_offset20(self):
        response = self.client.get('/api/posts/?limit=10&offset=20')

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            'Status 200 for get all posts')
        self.assertEqual(response.data['count'], self.post_count, 
            f'Posts total count should be as generated {self.post_count}')
        self.assertEqual(len(response.data['results']), 2,
            f'Posts actual count should be 2')

    def test_get_post_by_existing_id(self):
        response = self.client.get('/api/posts/4/')

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            'Status 200 for get existing post')
        self.assertTrue(response.data, 
            'Should return post data')

    def test_get_post_by_non_existing_id(self):
        response = self.client.get('/api/posts/100/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
            'Status 404 if post with given id is not exists')
        self.assertFalse(response.data, 
            'Should not return any data')

    def test_create_post_with_auth(self):
        data = {'title': 'test title', 'body': 'test body'}
        response = self.client.post('/api/posts/', data=data, HTTP_AUTHORIZATION=f'Token {self.token}')
        created_post = Post.objects.get(title='test title')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            'Status 201 if data is correct and authorized')
        self.assertEqual(created_post.title, response.data['title'], 
            'Created and received post titles should match')
        self.assertEqual(created_post.body, response.data['body'], 
            'Created and received post bodies should match')
        self.assertEqual(created_post.author, self.user, 
            'Created post author should match sender')

    def test_create_post_without_auth(self):
        data = {'title': 'not created', 'body': 'not created'}
        response = self.client.post('/api/posts/', data=data, HTTP_AUTHORIZATION='wrong token')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 
            'Status 401 if not authorized')
        self.assertFalse(Post.objects.filter(title='not created').exists(),
            'Post should not be created in DB')
        
class CommentsTestCase(APITestCase):
    username = 'test_user'
    password = 'strong_pass'
    post = None
    user = None
    token = None
    comments_count = 22

    def setUp(self) -> None:
        self.user = User.objects.create(username=self.username)
        self.user.set_password(self.password)
        self.user.save()

        self.post = Post.objects.create(title='test title', body='test body', author=self.user)
        self.post.save()

        for i in range(self.comments_count):
            comment = Comment.objects.create(author=self.user, post=self.post, body=f'test comment {i}')
            comment.save()

        # get token before leaving comments
        response = self.client.post('/api/auth/login/', data={'username': self.username, 'password': self.password})
        self.token = response.data['token']

    def test_get_all_comments_without_query_params(self):
        response = self.client.get(f'/api/comments/{self.post.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            'Status 200 for getting comments')
        self.assertEqual(response.data['count'], self.comments_count, 
            f'Comments total count should be as generated {self.comments_count}')
        self.assertEqual(len(response.data['results']), api_settings.PAGE_SIZE,
            f'Comments actual count should be as defined in PAGE_SIZE={api_settings.PAGE_SIZE}')

    def test_get_all_comments_limit10_offset_20(self):
        response = self.client.get(f'/api/comments/{self.post.id}/?limit=10&offset=20')

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            'Status 200 for getting comments')
        self.assertEqual(response.data['count'], self.comments_count, 
            f'Comments total count should be as generated {self.comments_count}')
        self.assertEqual(len(response.data['results']), 2,
            'Comments actual count should be 2')

    def test_create_comment_with_auth(self):
        data = {'body': 'test comment body'}
        response = self.client.post(f'/api/comments/{self.post.id}/', data, HTTP_AUTHORIZATION=f'Token {self.token}')
        created_comment = Comment.objects.get(body='test comment body')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            'Status 201 if data is correct and authorized')
        self.assertEqual(created_comment.body, response.data['body'], 
            'Created and received comment bodies should match')
        self.assertEqual(created_comment.post, self.post, 
            'Created and received comment post should match')
        self.assertEqual(created_comment.author, self.user, 
            'Created comment author should match sender')

    def test_create_comment_without_auth(self):
        data = {'body': 'not created'}
        response = self.client.post(f'/api/comments/{self.post.id}/', data=data, HTTP_AUTHORIZATION='wrong token')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, 
            'Status 401 if not authorized')
        self.assertFalse(Post.objects.filter(body='not created').exists(),
            'Post should not be created in DB')

class UserTestCase(APITestCase):
    username = 'test_user'
    password = 'strong_pass'
    user = None
    token = None

    def setUp(self) -> None:
        self.user = User.objects.create(username=self.username)
        self.user.set_password(self.password)
        self.user.save()

        # get token before fetch user
        response = self.client.post('/api/auth/login/', data={'username': self.username, 'password': self.password})
        self.token = response.data['token']

    def test_authorized_user_can_fetch_himself(self):
        response = self.client.get('/api/auth/user/', HTTP_AUTHORIZATION=f'Token {self.token}')

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            'Status 200 for fetching authorized user')
        self.assertEqual(response.data['username'], self.username,
            'Fetched and actual username should match')

    def test_unauthorized_user_cannot_fetch_himself(self):
        response = self.client.get('/api/auth/user/', HTTP_AUTHORIZATION='wrong token')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
            'Status 401 for unauthorized user')

class LogoutTestCase(APITestCase):
    username = 'test_user'
    password = 'strong_pass'
    user = None
    token = None

    def setUp(self) -> None:
        self.user = User.objects.create(username=self.username)
        self.user.set_password(self.password)
        self.user.save()

        # get token before fetch user
        response = self.client.post('/api/auth/login/', data={'username': self.username, 'password': self.password})
        self.token = response.data['token']

    def test_authorized_user_can_logout(self):
        responseLogout = self.client.post('/api/auth/logout/', HTTP_AUTHORIZATION=f'Token {self.token}')
        responseCreatePost = self.client.post('/api/posts/', HTTP_AUTHORIZATION=f'Token {self.token}')

        self.assertEqual(responseLogout.status_code, status.HTTP_204_NO_CONTENT,
            'Status 204 for successful logout')
        self.assertEqual(responseCreatePost.status_code, status.HTTP_401_UNAUTHORIZED,
            'Status 401 if trying to create post with old token')

    def test_unauthorized_user_cannot_logout(self):
        response = self.client.post('/api/auth/logout/', HTTP_AUTHORIZATION='wrong token')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED,
            'Status 401 if trying to logout without appropriate token')