from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Expense, ExpensesGroup
from sources.models import Source
from rest_framework.test import APIClient

class ExpensesGroupModelTests(TestCase):
    
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

        # Create expenses groups
        test_expgroup01 = ExpensesGroup.objects.create(
            user_id=test_user01,
            expgroup_name='expgroup01_testuser01', 
        )
        test_expgroup01.save()

        test_expgroup02 = ExpensesGroup.objects.create(
            user_id=test_user01,
            expgroup_name='expgroup02_testuser01', 
        )
        test_expgroup02.save()

    
    def test_expenses_group_content(self):
        # Test content
        expgroup = ExpensesGroup.objects.get(id=1)
        expected_object_name = f'{expgroup.expgroup_name}'
        self.assertEqual(expected_object_name, 'expgroup01_testuser01')

    def test_expenses_group_list_with_loggedin_user(self):
        # Test API get detailed with logged user
        client = APIClient()
        login = client.login(username='testuser01', password='testpass123')
        self.assertTrue(login)

        response = client.get('/api/v1/expenses/groups/', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        expected_object_name = f'{response.data[0]["expgroup_name"]}'
        self.assertEqual(expected_object_name, 'expgroup01_testuser01')

        client.logout()
        response = client.get('/api/v1/expenses/groups/', format='json')
        self.assertEqual(response.status_code, 403)

    def test_expenses_group_detail_with_loggedin_user(self):
        # Test API get list with logged user
        client = APIClient()
        login = client.login(username='testuser01', password='testpass123')
        self.assertTrue(login)

        response = client.get('/api/v1/expenses/groups/', format='json')
        id_lst = [entry["id"] for entry in response.data]
        expgroup_name = response.data[0]["expgroup_name"]
        response = client.get(f'/api/v1/expenses/groups/{id_lst[0]}/', format='json')
        self.assertEqual(response.status_code, 200)

        expected_object_name = f'{response.data["expgroup_name"]}'
        self.assertEqual(expected_object_name, expgroup_name)

        login = client.login(username='testuser02', password='testpass123')
        response = client.get(f'/api/v1/expenses/groups/{id_lst[0]}/', format='json')
        self.assertEqual(response.status_code, 404)

        client.logout()
        response = client.get('/api/v1/expenses/groups/1/', format='json')
        self.assertEqual(response.status_code, 403)

    def test_expenses_group_create_with_loggedin_user(self):
        # Test API create with loggedin user + loggedout user
        client = APIClient()
        login = client.login(username='testuser02', password='testpass123')
        self.assertTrue(login)
        post = client.post(
            '/api/v1/expenses/groups/', 
            {
                'expgroup_name': 'expgroup01_testuser02',
            }, 
            format='json'
        )
        self.assertEqual(post.status_code, 201)
        expgroup = ExpensesGroup.objects.last()
        expected_object_name = f'{expgroup.expgroup_name}'
        self.assertEqual(expected_object_name, 'expgroup01_testuser02')

        client.logout()
        post = client.post(
            '/api/v1/expenses/groups/', 
            {
                'expgroup_name': 'expgroup01_testuser02',
            }, 
            format='json'
        )
        self.assertEqual(post.status_code, 403)



class ExpensesModelTests(TestCase):
    
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

        # Create expenses groups
        test_expgroup01 = ExpensesGroup.objects.create(
            user_id=test_user01,
            expgroup_name='expgroup01_testuser01', 
        )
        test_expgroup01.save()

        test_expgroup02 = ExpensesGroup.objects.create(
            user_id=test_user02,
            expgroup_name='expgroup01_testuser02', 
        )
        test_expgroup02.save()

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

        # Create expenses
        test_expense01 = Expense.objects.create(
            user_id=test_user01,
            expense_name='expense01_testuser01',
            expense_value='101.01',
            expense_date='2021-01-21',
            expense_group=test_expgroup01,
            expense_source=test_source01,            
        )
        test_expense01.save()
        
        test_expense02 = Expense.objects.create(
            user_id=test_user01,
            expense_name='expense02_testuser01',
            expense_value='202.01',
            expense_date='2021-01-21',
            expense_group=test_expgroup01,
            expense_source=test_source01,            
        )
        test_expense02.save()

    def test_expense_content(self):
        # Test content
        expense = Expense.objects.get(id=1)
        expected_object_name = f'{expense.expense_name}'
        expected_object_value = f'{expense.expense_value}'
        expected_object_date = f'{expense.expense_date}'
        expected_object_expgroup = f'{expense.expense_group}'
        expected_object_source = f'{expense.expense_source}'

        self.assertEqual(expected_object_name, 'expense01_testuser01')
        self.assertEqual(expected_object_value, '101.01')
        self.assertEqual(expected_object_date, '2021-01-21')
        self.assertEqual(expected_object_expgroup, 'expgroup01_testuser01')
        self.assertEqual(expected_object_source, 'source01_testuser01')

    def test_expense_list_with_loggedin_user(self):
        # Test API get detailed with logged user
        client = APIClient()
        login = client.login(username='testuser01', password='testpass123')
        self.assertTrue(login)

        response = client.get('/api/v1/expenses/', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        expected_object_name = f'{response.data[0]["expense_name"]}'
        expected_object_value = f'{response.data[0]["expense_value"]}'
        expected_object_date = f'{response.data[0]["expense_date"]}'

        expgroup_id = f'{response.data[0]["expense_group"]}'
        expgroup = ExpensesGroup.objects.get(id=expgroup_id)
        expected_object_expgroup = f'{expgroup.expgroup_name}'

        source_id = f'{response.data[0]["expense_source"]}'
        source = Source.objects.get(id=source_id)
        expected_object_source= f'{source.source_name}'

        self.assertEqual(expected_object_name, 'expense01_testuser01')
        self.assertEqual(expected_object_value, '101.01')
        self.assertEqual(expected_object_date, '2021-01-21')
        self.assertEqual(expected_object_expgroup, 'expgroup01_testuser01')
        self.assertEqual(expected_object_source, 'source01_testuser01')

        client.logout()
        response = client.get('/api/v1/expenses/', format='json')
        self.assertEqual(response.status_code, 403)

    def test_expense_detail_with_loggedin_user(self):
        # Test API get list with logged user
        client = APIClient()
        login = client.login(username='testuser01', password='testpass123')
        self.assertTrue(login)

        response = client.get('/api/v1/expenses/', format='json')
        id_lst = [entry["id"] for entry in response.data]
        expense_name = response.data[0]["expense_name"]
        expense_value = response.data[0]["expense_value"]
        expense_date = response.data[0]["expense_date"]
        expense_group = response.data[0]["expense_group"]
        expense_source = response.data[0]["expense_source"]

        response = client.get(f'/api/v1/expenses/{id_lst[0]}/', format='json')
        self.assertEqual(response.status_code, 200)

        expected_object_name = f'{response.data["expense_name"]}'
        expected_object_value = f'{response.data["expense_value"]}'
        expected_object_date = f'{response.data["expense_date"]}'
        expected_object_expgroup = f'{response.data["expense_group"]}'
        expected_object_source = f'{response.data["expense_source"]}'

        self.assertEqual(expected_object_name, expense_name)
        self.assertEqual(expected_object_value, expense_value)
        self.assertEqual(expected_object_date, expense_date)
        self.assertEqual(expected_object_expgroup, str(expense_group))
        self.assertEqual(expected_object_source, str(expense_source))

        login = client.login(username='testuser02', password='testpass123')
        response = client.get(f'/api/v1/expenses/groups/{id_lst[0]}/', format='json')
        self.assertEqual(response.status_code, 404)

        client.logout()
        response = client.get('/api/v1/expenses/groups/1/', format='json')
        self.assertEqual(response.status_code, 403)

    def test_expenses_create_with_loggedin_user(self):
        # Test API create with loggedin user + loggedout user
        client = APIClient()
        login = client.login(username='testuser02', password='testpass123')
        self.assertTrue(login)

        response = client.get('/api/v1/expenses/groups/', format='json')
        expgroup_idlst = [entry["id"] for entry in response.data]
        expgroup = ExpensesGroup.objects.get(id=expgroup_idlst[0])

        response = client.get('/api/v1/sources/', format='json')
        source_idlst = [entry["id"] for entry in response.data]
        source = Source.objects.get(id=source_idlst[0])


        post = client.post(
            '/api/v1/expenses/', 
            {
                'expense_name':'expense01_testuser02',
                'expense_value': '101.02',
                'expense_date': '2021-01-21',
                'expense_group': expgroup.id,
                'expense_source': source.id,            
            }, 
            format='json'
        )
        self.assertEqual(post.status_code, 201)

        expense = Expense.objects.last()
        expected_object_name = f'{expense.expense_name}'
        expected_object_name = f'{expense.expense_name}'
        expected_object_value = f'{expense.expense_value}'
        expected_object_date = f'{expense.expense_date}'
        expected_object_expgroup = f'{expense.expense_group}'
        expected_object_source = f'{expense.expense_source}'
        self.assertEqual(expected_object_name, 'expense01_testuser02')
        self.assertEqual(expected_object_value, '101.02')
        self.assertEqual(expected_object_date, '2021-01-21')
        self.assertEqual(expected_object_expgroup, 'expgroup01_testuser02')
        self.assertEqual(expected_object_source, 'source01_testuser02')

        expgroup = ExpensesGroup.objects.get(expgroup_name='expgroup01_testuser01')
        post = client.post(
            '/api/v1/expenses/', 
            {
                'expense_name':'expense01_testuser02',
                'expense_value': '101.02',
                'expense_date': '2021-01-21',
                'expense_group': expgroup.id,
                'expense_source': source.id,            
            }, 
            format='json'
        )
        self.assertEqual(post.status_code, 400)
        self.assertEqual(post.data[0], 'This expense group is not defined in your account')

        client.logout()
        expgroup = ExpensesGroup.objects.get(expgroup_name='expgroup01_testuser02')
        post = client.post(
            '/api/v1/expenses/', 
            {
                'expense_name':'expense01_testuser02',
                'expense_value': '101.02',
                'expense_date': '2021-01-21',
                'expense_group': expgroup.id,
                'expense_source': source.id,            
            }, 
            format='json'
        )
        self.assertEqual(post.status_code, 403)

