import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()
from rest_framework.test import  APITestCase
from todos.models.models import ToDo
from rest_framework import status
from users.models import CustomUser
from django.urls import reverse
import copy


class ToDoTest(APITestCase):

    def log_user(self, email= None, password = None):

        # login url
        url = '/users/dj-rest-auth/login/'

        # login details
        credentials = {
            "email": email,
            "password": password
        }

        # log user in
        response = self.client.post(url, data=credentials, format='multipart')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # check that a token has been generated
        access_token = response.data.get('access_token', None)
        self.assertTrue(access_token is not None)

        return access_token

    def setUp(self):

        client = self.client

        # create user
        user = CustomUser.objects.create_user(
            username = 'titi',
            password = 'victoire',
            email='titi@flatters.com'
        )
        user.save()

        # log user
        access_token = self.log_user(email='titi@flatters.com', password='victoire')

        # create 2 todos
        data=[
            {"title": "buy milk", "description": "6 L", "completed": False},
            {"title": "feed the cat", "description": "give it meat balls", "completed": True},
        ]
        todos=list()
        for data_item  in data:
            todo = ToDo(title=data_item["title"], description=data_item["description"], completed=data_item["completed"], creator=user)
            todo.save()
            todos.append(todo)

        # save data
        self.logged_user = user
        self.client = client
        self.todos = todos
        self.access_token = access_token

    def tearDown(self):
        self.client.logout()


    def test_create(self):

        access_token = self.access_token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + access_token)

        expected_list=[
            {"title": "go to the swimming pool", "description": "swim during 1 hour", "completed": False},
        ]

        url = reverse('todos:list')

        for expected in expected_list:
            data = copy.deepcopy(expected)
            response = self.client.post(url, data=data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            todos = ToDo.objects.filter(title=expected["title"])
            self.assertEqual(todos.count(),1)


    def test_delete(self):

        # get all users in database
        todos = ToDo.objects.all()

        # delete all users in test database save for the logged one
        for todo in todos:
            url = reverse('todos:detail', args={todo.pk})
            response = self.client.delete(url, format='multipart')
            self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        # check that all users in database have been deleted save for the logged one
        todos = ToDo.objects.all()
        self.assertEqual(todos.count(), 0)


    def test_detail(self):

        # unpack data
        todos = self.todos

        for id, todo in enumerate(todos):
            expected = {
                'id': todo.id,
                'title': todo.title,
                'description': todo.description,
                'completed': todo.completed,
                'creator': todo.creator.email
            }
            url = reverse('todos:detail', args={expected['id']})
            response = self.client.get(url,  format='multipart')
            results = response.data
            self.assertEqual(status.HTTP_200_OK, response.status_code)
            self.assertTrue(expected.items() <= results.items()) # check that expected_user is a sub dictionary of actual_user


    def test_edit(self):

        # unpack data
        todos = self.todos

        for todo in todos:
            # get snippet data
            url = reverse('todos:detail', args={todo.pk})
            response = self.client.get(url, format='json')
            original_data = response.data
            expected = copy.deepcopy(original_data)
            expected["description"] += " - after edition"
            expected.pop('last_edited')
            expected['last_editor']=self.logged_user.email

            url = reverse('todos:detail',  args={todo.id})
            response = self.client.put(url, expected, format='json')
            results = response.data
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

            url = reverse('todos:detail', args={todo.pk})
            results = self.client.get(url, format='json').data
            print("expected: ", expected)
            print("results: ", results)
            self.assertTrue(expected.items() <= results.items())


    def test_list(self):

        # unpack data
        todos = self.todos

        expected = list()
        for todo in todos:
            expected_item = dict(
                title = todo.title,
                description = todo.description,
                completed = todo.completed
            )
            expected += [expected_item]

        url = reverse('todos:list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for id, results in enumerate(response.data):
            results = dict(results)
            results.pop("id")
            print(expected[id].items())
            print( results.items())
            self.assertTrue(expected[id].items() <= results.items())
