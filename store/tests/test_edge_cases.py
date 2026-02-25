from django.test import TestCase,Client
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Product,Category

class CartEdgeCaseTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username = 'testuser',
            password = 'testpass123'
        )

        self.category = Category.objects.create(name="Tea")
        self.product = Product.objects.create(
            name = "Green Tea",
            price = 259.99,
            category = self.category
        )

        self.cart_url = reverse('cart_view')
        self.add_to_cart_url = reverse('add_to_cart',args = [self.product.id])
        self.client = Client()

    def test_cart_with_deleted_product(self):
        self.client.login(username='testuser',password = 'testpass123')
        self.client.post(self.add_to_cart_url)
        product_id = self.product.id
        self.product.delete()

        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code,200)