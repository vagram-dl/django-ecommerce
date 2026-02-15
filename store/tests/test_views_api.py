from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase,APIClient
from rest_framework import status
from django.contrib.auth.models import User
from store.models import Category, Product
from decimal import Decimal

class ProductViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='regular_user',
            password = 'password123'
        )

        self.admin_user = User.objects.create_superuser(
            username='admin_user',
            password = 'admin123',
            email='admin@example.com'
        )

        self.category_tea = Category.objects.create(
            name="Tea",
            slug = "tea"
        )


        self.category_coffee = Category.objects.create(
           name = "Coffee",
            slug = "coffee"
        )

        self.product1 = Product.objects.create(
            name = "Green Tea",
            price = 259.99,
            category = self.category_tea,
            description = "Healthy green tea"
        )

        self.product2 = Product.objects.create(
            name = "Black Tea",
            price = 199.99,
            category = self.category_tea
        )

        self.client = APIClient()
        self.products_url = reverse('product-list')

    def test_list_products_unauthenticated(self):
        response = self.client.get(self.products_url)

        results = response.data['results']
        self.assertEqual(len(results), 2)

        product_names = [product['name'] for product in results]
        self.assertIn('Green Tea', product_names)
        self.assertIn('Black Tea', product_names)

    def test_filter_products_by_category(self):
        product_coffee = Product.objects.create(
            name = "Espresso",
            price = 399.99,
            category = self.category_coffee
        )

        url = f"{self.products_url}?category__slug=tea"
        print(f"URL запроса : {url}")
        response = self.client.get(url)
        print(f"Статус ответа : {response.status_code}")
        print(f"Count:{response.data['count']}")
        print(f"Results: {[p['name'] for p in response.data['results']]}")

        self.assertEqual(response.status_code,200)

        results = response.data['results']
        product_names = [product['name'] for product in results]

        self.assertEqual(len(results),2)
        self.assertIn('Green Tea',product_names)
        self.assertIn('Black Tea',product_names)
        self.assertNotIn('Espresso',product_names)

        self.assertEqual(response.data['count'],2)

    def test_retrieve_product_detail(self):
        url = reverse('product-detail',args=[self.product1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data['name'],'Green Tea')
        self.assertEqual(response.data['price'],'259.99')
        self.assertEqual(response.data['category'],self.category_tea.id)

    def test_retrieve_product_not_found(self):
        url = reverse('product-detail',args=[999])
        response = self.client.get(url)

        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def test_create_product_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)

        new_product = {
            'name' : 'Oolong Tea',
            'price':'350.00',
            'category':self.category_tea.id,
            'description':'Traditional Chinese tea'
        }

        response = self.client.post(self.products_url,new_product,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(),3)

        new_product_db = Product.objects.get(name='Oolong Tea')
        self.assertEqual(new_product_db.price,350.00)
        self.assertEqual(new_product_db.category,self.category_tea)
        self.assertEqual(new_product_db.description, 'Traditional Chinese tea')

        self.assertEqual(response.data['name'],'Oolong Tea')
        self.assertEqual(response.data['price'],'350.00')

