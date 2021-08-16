from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Income, IncomesGroup 
from sources.models import Source
from rest_framework.test import APIClient

class IncomesGroupModelTests(TestCase):
    
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

        # Create incomes groups
        test_incgroup01 = IncomesGroup.objects.create(
            user_id=test_user01,
            incgroup_name='incgroup01_testuser01', 
        )
        test_incgroup01.save()

        test_incgroup02 = IncomesGroup.objects.create(
            user_id=test_user01,
            incgroup_name='incgroup02_testuser01', 
        )
        test_incgroup02.save()

    
    def test_incomes_group_content(self):
        # Test content
        incgroup = IncomesGroup.objects.get(id=1)
        expected_object_name = f'{incgroup.incgroup_name}'
        self.assertEqual(expected_object_name, 'incgroup01_testuser01')
        
    def test_incomes_group_list_with_loggedin_user(self):
        # Test API get detailed with logged user
        client = APIClient()
        login = client.login(username='testuser01', password='testpass123')
        self.assertTrue(login)

        response = client.get('/api/v1/incomes/groups/', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        expected_object_name = f'{response.data[0]["incgroup_name"]}'
        self.assertEqual(expected_object_name, 'incgroup01_testuser01')

        client.logout()
        response = client.get('/api/v1/incomes/groups/', format='json')
        self.assertEqual(response.status_code, 403)

    def test_incomes_group_detail_with_loggedin_user(self):
        # Test API get list with logged user
        client = APIClient()
        login = client.login(username='testuser01', password='testpass123')
        self.assertTrue(login)

        response = client.get('/api/v1/incomes/groups/', format='json')
        id_lst = [entry["id"] for entry in response.data]
        incgroup_name = response.data[0]["incgroup_name"]
        response = client.get(f'/api/v1/incomes/groups/{id_lst[0]}/', format='json')
        self.assertEqual(response.status_code, 200)

        expected_object_name = f'{response.data["incgroup_name"]}'
        self.assertEqual(expected_object_name, incgroup_name)

        login = client.login(username='testuser02', password='testpass123')
        response = client.get(f'/api/v1/incomes/groups/{id_lst[0]}/', format='json')
        self.assertEqual(response.status_code, 404)

        client.logout()
        response = client.get('/api/v1/incomes/groups/1/', format='json')
        self.assertEqual(response.status_code, 403)

    def test_incomes_group_create_with_loggedin_user(self):
        # Test API create with loggedin user + loggedout user
        client = APIClient()
        login = client.login(username='testuser02', password='testpass123')
        self.assertTrue(login)
        post = client.post(
            '/api/v1/incomes/groups/', 
            {
                'incgroup_name': 'incgroup01_testuser02',
            }, 
            format='json'
        )
        self.assertEqual(post.status_code, 201)
        incgroup = IncomesGroup.objects.last()
        expected_object_name = f'{incgroup.incgroup_name}'
        self.assertEqual(expected_object_name, 'incgroup01_testuser02')

        client.logout()
        post = client.post(
            '/api/v1/incomes/groups/', 
            {
                'incgroup_name': 'incgroup01_testuser02',
            }, 
            format='json'
        )
        self.assertEqual(post.status_code, 403)


class IncomesModelTests(TestCase):
    
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

        # Create incomes groups
        test_incgroup01 = IncomesGroup.objects.create(
            user_id=test_user01,
            incgroup_name='incgroup01_testuser01', 
        )
        test_incgroup01.save()

        test_incgroup02 = IncomesGroup.objects.create(
            user_id=test_user02,
            incgroup_name='incgroup01_testuser02', 
        )
        test_incgroup02.save()

        # Create sources groups
        test_source01 = Source.objects.create(
            user_id=test_user01,
            source_name='source01_testuser01', 
            source_value='101.01',
        )
        test_source01.save()

        test_source02 = Source.objects.create(
            user_id=test_user02,
            source_name='source01_testuser02', 
            source_value='101.02',
        )
        test_source02.save()

        # Create incomes 
        test_income01 = Income.objects.create(
            user_id=test_user01,
            income_name='income01_testuser01',
            income_value='101.01',
            income_date='2021-01-21',
            income_group=test_incgroup01,
            income_source=test_source01,            
        )
        test_income01.save()
        
        test_income02 = Income.objects.create(
            user_id=test_user01,
            income_name='income02_testuser01',
            income_value='202.01',
            income_date='2021-01-21',
            income_group=test_incgroup01,
            income_source=test_source01,            
        )
        test_income02.save()

    def test_income_content(self):
        # Test content
        income = Income.objects.get(id=1)
        expected_object_name = f'{income.income_name}'
        expected_object_value = f'{income.income_value}'
        expected_object_date = f'{income.income_date}'
        expected_object_incgroup = f'{income.income_group}'
        expected_object_source = f'{income.income_source}'

        self.assertEqual(expected_object_name, 'income01_testuser01')
        self.assertEqual(expected_object_value, '101.01')
        self.assertEqual(expected_object_date, '2021-01-21')
        self.assertEqual(expected_object_incgroup, 'incgroup01_testuser01')
        self.assertEqual(expected_object_source, 'source01_testuser01')

    def test_income_list_with_loggedin_user(self):
        # Test API get detailed with logged user
        client = APIClient()
        login = client.login(username='testuser01', password='testpass123')
        self.assertTrue(login)

        response = client.get('/api/v1/incomes/', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        expected_object_name = f'{response.data[0]["income_name"]}'
        expected_object_value = f'{response.data[0]["income_value"]}'
        expected_object_date = f'{response.data[0]["income_date"]}'

        incgroup_id = f'{response.data[0]["income_group"]}'
        incgroup = IncomesGroup.objects.get(id=incgroup_id)
        expected_object_incgroup = f'{incgroup.incgroup_name}'

        source_id = f'{response.data[0]["income_source"]}'
        source = Source.objects.get(id=source_id)
        expected_object_source= f'{source.source_name}'

        self.assertEqual(expected_object_name, 'income01_testuser01')
        self.assertEqual(expected_object_value, '101.01')
        self.assertEqual(expected_object_date, '2021-01-21')
        self.assertEqual(expected_object_incgroup, 'incgroup01_testuser01')
        self.assertEqual(expected_object_source, 'source01_testuser01')

        client.logout()
        response = client.get('/api/v1/incomes/', format='json')
        self.assertEqual(response.status_code, 403)

    def test_income_detail_with_loggedin_user(self):
        # Test API get list with logged user
        client = APIClient()
        login = client.login(username='testuser01', password='testpass123')
        self.assertTrue(login)

        response = client.get('/api/v1/incomes/', format='json')
        id_lst = [entry["id"] for entry in response.data]
        income_name = response.data[0]["income_name"]
        income_value = response.data[0]["income_value"]
        income_date = response.data[0]["income_date"]
        income_group = response.data[0]["income_group"]
        income_source = response.data[0]["income_source"]

        response = client.get(f'/api/v1/incomes/{id_lst[0]}/', format='json')
        self.assertEqual(response.status_code, 200)

        expected_object_name = f'{response.data["income_name"]}'
        expected_object_value = f'{response.data["income_value"]}'
        expected_object_date = f'{response.data["income_date"]}'
        expected_object_incgroup = f'{response.data["income_group"]}'
        expected_object_source = f'{response.data["income_source"]}'

        self.assertEqual(expected_object_name, income_name)
        self.assertEqual(expected_object_value, income_value)
        self.assertEqual(expected_object_date, income_date)
        self.assertEqual(expected_object_incgroup, str(income_group))
        self.assertEqual(expected_object_source, str(income_source))

        login = client.login(username='testuser02', password='testpass123')
        response = client.get(f'/api/v1/incomes/groups/{id_lst[0]}/', format='json')
        self.assertEqual(response.status_code, 404)

        client.logout()
        response = client.get('/api/v1/incomes/groups/1/', format='json')
        self.assertEqual(response.status_code, 403)

    def test_incomes_create_with_loggedin_user(self):
        # Test API create with loggedin user + loggedout user
        client = APIClient()
        login = client.login(username='testuser02', password='testpass123')
        self.assertTrue(login)

        response = client.get('/api/v1/incomes/groups/', format='json')
        incgroup_idlst = [entry["id"] for entry in response.data]
        incgroup = IncomesGroup.objects.get(id=incgroup_idlst[0])

        response = client.get('/api/v1/sources/', format='json')
        source_idlst = [entry["id"] for entry in response.data]
        source = Source.objects.get(id=source_idlst[0])


        post = client.post(
            '/api/v1/incomes/', 
            {
                'income_name':'income01_testuser02',
                'income_value': '101.02',
                'income_date': '2021-01-21',
                'income_group': incgroup.id,
                'income_source': source.id,            
            }, 
            format='json'
        )
        self.assertEqual(post.status_code, 201)

        income = Income.objects.last()
        expected_object_name = f'{income.income_name}'
        expected_object_name = f'{income.income_name}'
        expected_object_value = f'{income.income_value}'
        expected_object_date = f'{income.income_date}'
        expected_object_incgroup = f'{income.income_group}'
        expected_object_source = f'{income.income_source}'
        self.assertEqual(expected_object_name, 'income01_testuser02')
        self.assertEqual(expected_object_value, '101.02')
        self.assertEqual(expected_object_date, '2021-01-21')
        self.assertEqual(expected_object_incgroup, 'incgroup01_testuser02')
        self.assertEqual(expected_object_source, 'source01_testuser02')

        incgroup = IncomesGroup.objects.get(incgroup_name='incgroup01_testuser01')
        post = client.post(
            '/api/v1/incomes/', 
            {
                'income_name':'income01_testuser02',
                'income_value': '101.02',
                'income_date': '2021-01-21',
                'income_group': incgroup.id,
                'income_source': source.id,            
            }, 
            format='json'
        )
        self.assertEqual(post.status_code, 400)
        self.assertEqual(post.data[0], 'This income group is not defined in your account')

        client.logout()
        incgroup = IncomesGroup.objects.get(incgroup_name='incgroup01_testuser02')
        post = client.post(
            '/api/v1/incomes/', 
            {
                'income_name':'income01_testuser02',
                'income_value': '101.02',
                'income_date': '2021-01-21',
                'income_group': incgroup.id,
                'income_source': source.id,            
            }, 
            format='json'
        )
        self.assertEqual(post.status_code, 403)