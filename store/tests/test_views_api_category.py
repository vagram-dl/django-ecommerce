from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase,APIClient
from rest_framework import status
from django.contrib.auth.models import User
from store.models import Category

class CategoryViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = 'regular_user',
            password = 'password123'
        )

        self.admin_user = User.objects.create_superuser(
            username = 'admin_user',
            password = 'admin123',
            email = 'admin@example.com'
        )

        self.category_tea = Category.objects.create(
            name = "Tea",
            slug = "tea",
            description = "All kinds of tea"
        )

        self.category_coffee = Category.objects.create(
            name = "Coffee",
            slug = "coffee"
        )

        self.category_green_tea = Category.objects.create(
            name = "Green Tea",
            parent = self.category_tea
        )

        self.client = APIClient()
        self.categories_url = reverse('category-list')

    def test_list_categories(self):
        response = self.client.get(self.categories_url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results),3)
        category_names = [cat['name'] for cat in results]
        self.assertIn('Tea',category_names)
        self.assertIn('Coffee',category_names)
        self.assertIn('Green Tea',category_names)

        for cat in results:
            if cat['name'] == 'Tea':
                self.assertEqual(cat['slug'],'tea')
            elif cat['name'] == 'Coffee':
                self.assertEqual(cat['slug'],'coffee')