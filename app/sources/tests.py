from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Source
from rest_framework.test import APIClient

class SourceGroupModelTests(TestCase):
    
    def setUp(self):
        # Create users
        test_user01 = get_user_model().objects.create_user(
            username="testuser01",
            email="testuser01@email.com",
            password="testpass123",
        )
        test_user01.save()

        test_user02 = get_user_model().objects.create_user(
            username="testuser02",
            email="testuser02@email.com",
            password="testpass123",
        )
        test_user02.save()

        # Create sources
        test_source01 = Source.objects.create(
            user_id=test_user01,
            source_name='source01_testuser01', 
            source_value='101.01',
        )
        test_source01.save()

        test_source02 = Source.objects.create(
            user_id=test_user01,
            source_name='source02_testuser01', 
            source_value='202.02',
        )
        test_source02.save()
    
    def test_source_content(self):
        # Test content
        id = Source.objects.first().id
        source = Source.objects.get(id=id)
        expected_object_name = f'{source.source_name}'
        expected_object_value = f'{source.source_value}'
        self.assertEqual(expected_object_name, 'source01_testuser01')
        self.assertEqual(expected_object_value, '101.01')

    def test_source_list_with_loggedin_user(self):
        # Test API get detailed with logged user
        client = APIClient()
        login = client.login(username='testuser01', password='testpass123')
        self.assertTrue(login)

        response = client.get('/api/v1/sources/', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        expected_object_name = f'{response.data[0]["source_name"]}'
        expected_object_value = f'{response.data[0]["source_value"]}'
        self.assertEqual(expected_object_name, 'source01_testuser01')
        self.assertEqual(expected_object_value, '101.01')

        client.logout()
        response = client.get('/api/v1/sources/', format='json')
        self.assertEqual(response.status_code, 403)

    def test_source_group_detail_with_loggedin_user(self):
        # Test API get list with logged user
        client = APIClient()
        login = client.login(username='testuser01', password='testpass123')
        self.assertTrue(login)

        response = client.get('/api/v1/sources/', format='json')
        id_lst = [entry["id"] for entry in response.data]
        source_name = response.data[0]["source_name"]
        source_value = response.data[0]["source_value"]
        response = client.get(f'/api/v1/sources/{id_lst[0]}/', format='json')
        self.assertEqual(response.status_code, 200)

        expected_object_name = f'{response.data["source_name"]}'
        expected_object_value = f'{response.data["source_value"]}'
        self.assertEqual(expected_object_name, source_name)
        self.assertEqual(expected_object_value, source_value)

        login = client.login(username='testuser02', password='testpass123')
        response = client.get(f'/api/v1/expenses/groups/{id_lst[0]}/', format='json')
        self.assertEqual(response.status_code, 404)

        client.logout()
        response = client.get('/api/v1/expenses/groups/1/', format='json')
        self.assertEqual(response.status_code, 403)

    def test_source_group_create_with_loggedin_user(self):
        # Test API create with loggedin user + loggedout user
        client = APIClient()
        login = client.login(username='testuser02', password='testpass123')
        self.assertTrue(login)
        post = client.post(
            '/api/v1/sources/', 
            {
                'source_name': 'source01_testuser02',
                'source_value': '101.02',
            }, 
            format='json'
        )
        self.assertEqual(post.status_code, 201)
        source = Source.objects.last()
        expected_object_name = f'{source.source_name}'
        expected_object_value = f'{source.source_value}'
        self.assertEqual(expected_object_name, 'source01_testuser02')
        self.assertEqual(expected_object_value, '101.02')

        client.logout()
        post = client.post(
            '/api/v1/sources/', 
            {
                'source_name': 'source01_testuser02',
                'source_value': '101.02',
            }, 
            format='json'
        )
        self.assertEqual(post.status_code, 403)





    