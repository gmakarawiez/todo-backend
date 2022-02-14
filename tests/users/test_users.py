import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser
from django.urls import reverse
from django.contrib.auth import authenticate, login

class CustomUserTests(APITestCase):

    def setUp(self):
        this_dir = os.path.dirname(os.path.realpath(__file__))

        # Fill in the database with users
        expected_users = [
            {
                "username": "nemo",
                "email": "nemo@pacific.com",
                "password": "saJ@nq_Y4asB",
            },
            {
                "username": "dory",
                "email": "dory@pacific.com",
                "password": "Hqfd5%af'HqqM9",
            }
        ]

        for expected_user in expected_users:
            CustomUser.objects.create_user(**expected_user)

        self.expected_users = expected_users


    def tearDown(self):
        #self.client.logout()
        pass

    """
    def test_blacklist_token(self):

        # unpack data
        expected_users = self.expected_users

        # login url
        url = '/users/tokens/get'

        # login details
        data = expected_users[0]
        data.pop("username")

        # log user in
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # check that a token has been generated
        access_token = response.data.get('access', None)
        refresh_token = response.data.get('refresh', None)
        self.assertTrue(access_token is not None)
        self.assertTrue(refresh_token is not None)

        # check token validity
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + access_token)
        url = '/users/tokens/verify'
        data = {"token": access_token}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # blacklist token
        #self.client.credentials(HTTP_AUTHORIZATION='Token ' + access_token)
        url = '/users/tokens/blacklist'
        data = {"access": access_token, "refresh": refresh_token}
        response = self.client.post(url, data, format='multipart')
        #self.assertEqual(status.HTTP_200_OK, response.status_code)

        # check token validity
        #self.client.credentials(HTTP_AUTHORIZATION='Token ' + access_token)
        #url = '/users/tokens/verify'
        #data = {"token": access_token}
        #response = self.client.post(url, data, format='multipart')
        #print(response)
        #self.assertEqual(status.HTTP_200_OK, response.status_code)
    """

    def get_tokens(self):

        # unpack data
        expected_users = self.expected_users

        # login url
        url = '/users/dj-rest-auth/login/'

        # login details
        logged_user = expected_users[0]

        # log user in
        response = self.client.post(url, data=logged_user, format='multipart')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # check that a token has been generated
        access_token = response.data.get('access_token', None)
        self.assertTrue(access_token is not None)
        refresh_token = response.data.get('refresh_token', None)
        self.assertTrue(refresh_token is not None)

        return logged_user, access_token, refresh_token


    def test_delete(self):

        # get token
        logged_user, access_token, refresh_token = self.get_tokens()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + access_token)

        # get all users in database
        users = CustomUser.objects.all()

        # delete all users in test database save for the logged one
        for user in users:
            if user.email == logged_user["email"]:
                continue

            url = reverse('users:detail', args={user.pk})
            print(url)
            response = self.client.delete(url, format='multipart')
            print(response)
            self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        # check that all users in database have been deleted save for the logged one
        custom_users = CustomUser.objects.all()
        self.assertEqual(custom_users.count(), 1)
        self.assertEqual(custom_users[0].email, logged_user["email"])


    def test_detail(self):

        # unpack data
        expected_users = self.expected_users

        # get token
        logged_user, access_token, refresh_token = self.get_tokens()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + access_token)

        for id, expected_user in enumerate(expected_users):
            actual_id = CustomUser.objects.get(email = expected_user["email"]).id
            url = reverse('users:detail', args={actual_id})
            response = self.client.get(url,  format='multipart')
            actual_user = response.data
            self.assertEqual(status.HTTP_200_OK, response.status_code)
            expected_user.pop('password')
            actual_user.pop('password')
            self.assertTrue(expected_user.items() <= actual_user.items()) # check that expected_user is a sub dictionary of actual_user


    def test_edit(self):

        # unpack data
        original_users = self.expected_users

        # get token
        logged_user, access_token, refresh_token = self.get_tokens()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + access_token)

        # add suffix to the username of the users defined in test database
        expected_users = original_users
        for user in expected_users:
            user["username"] = user["username"] + "_edited"

        for id, expected_user in enumerate(expected_users):
            actual_id = CustomUser.objects.get(email = expected_user["email"]).id
            url = reverse('users:detail', args = {actual_id})
            response = self.client.put(url, expected_user, format='multipart')
            print("response.data: ", response.data)
            actual_user = response.data
            self.assertEqual(status.HTTP_200_OK, response.status_code)
            expected_user.pop('password')
            actual_user.pop('password')
            print(expected_user)
            print(actual_user)
            self.assertTrue(expected_user.items() <= actual_user.items()) # check that expected_user is a sub directory of actual_user

    """
    def test_get_current_user(self):

        # unpack data
        expected_users = self.expected_users

        # login url
        url = '/users/tokens/get'

        # login details
        logged_user = expected_users[0]
        logged_user.pop("username")

        # log user in
        response = self.client.post(url, data=logged_user, format='multipart')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # get current user
        url = reverse('users:current_user')
        response = self.client.get(url)
        actual_user = response.data

        self.assertEqual(logged_user["email"], actual_user["email"])
    """

    def test_list(self):

        # unpack data
        expected_users = self.expected_users

        # get users list
        url = reverse('users:list')
        response = self.client.get(url, format='multipart')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        actual_users= response.data
        print("actual_users", actual_users)

        # test users list
        for id, expected_user in enumerate(expected_users):
            actual_user = [actual_user for actual_user in actual_users if actual_user["username"]==expected_user["username"]][0]
            self.assertEqual(expected_user['email'], actual_user['email'])


    def test_login(self):

        # unpack data
        expected_users = self.expected_users

        # login url
        url = '/users/dj-rest-auth/login/'

        # login details
        data = expected_users[0]
        data.pop("username")

        # log user in
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # check that a token has been generated
        print(response.data)
        access_token = response.data.get('access_token', None)
        print("access_token=", access_token)
        self.assertTrue(access_token is not None)

        # check token validity
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + access_token)
        url = '/users/dj-rest-auth/token/verify/'
        data = {"token": access_token}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(status.HTTP_200_OK, response.status_code)


    def test_logout(self):

        # login url
        url = '/users/dj-rest-auth/logout/'

        # log user in
        response = self.client.post(url, format='multipart')
        self.assertEqual(status.HTTP_200_OK, response.status_code)


    def test_refresh_token(self):

        # get retfresh token
        logged_user, access_token, refresh_token = self.get_tokens()

        # registration url
        url = '/users/dj-rest-auth/token/refresh/'

        # registration details for new user
        data =  {
                 "refresh": refresh_token,
            }

        # register new user
        response = self.client.post(url, data=data, format='multipart')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        print(response.data)

    def test_registration(self):

        # registration url
        url = '/users/dj-rest-auth/registration/'

        # registration details for new user
        data =  {
                 "email": "nemo4@pacific.com",
                "password1": "saJ@nq_Y4asB",
                "password2": "saJ@nq_Y4asB",
                "username": "nemo4"
            }

        # register new user
        result = self.client.post(url, data=data, format='multipart')
        self.assertEqual(status.HTTP_201_CREATED, result.status_code)











