from django.test import TestCase
from django.contrib.auth import get_user_model


class CustomUserModelTest(TestCase):
    
    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
            id=1,
            username="testuser",
            email="testuser@email.com",
            password="testpass123",

        )
        self.test_user.save()

        self.test_superuser = get_user_model().objects.create_superuser(
            id=2,
            username="testsuperuser",
            email="testsuperuser@email.com",
            password="testpass123",

        )
        self.test_superuser.save()
    
    def test_create_user(self):
        # Test if user data is correctly saved
        user = get_user_model().objects.get(id=1)
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser(self):
        # Test if superuser data is correctly saved
        self.assertEqual(self.test_superuser.username, 'testsuperuser')
        self.assertEqual(self.test_superuser.email, 'testsuperuser@email.com')
        self.assertTrue(self.test_superuser.is_active)
        self.assertTrue(self.test_superuser.is_staff)
        self.assertTrue(self.test_superuser.is_superuser)
