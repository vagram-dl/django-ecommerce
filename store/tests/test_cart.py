from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Product,Category

class CartViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name = "Tea",
            slug = "tea"
        )

        self.product1 = Product.objects.create(
            name = "Green Tea",
            price = 259.99,
            category = self.category
        )

        self.product2 = Product.objects.create(
            name = "Black Tea",
            price = 199.99,
            category = self.category
        )

        self.cart_url = reverse('cart_view')
        self.add_to_cart_url = reverse('add_to_cart',args=[self.product1.id])

    def test_add_to_cart(self):
        response = self.client.post(self.add_to_cart_url)
        self.assertRedirects(response,reverse('cart_view'))

        session = self.client.session
        cart = session.get('cart',{})
        self.assertIn(str(self.product1.id),cart)
        self.assertEqual(cart[str(self.product1.id)],1)

    def test_add_existing_product_to_cart(self):
        self.client.post(self.add_to_cart_url)
        self.client.post(self.add_to_cart_url)
        session = self.client.session
        cart = session.get('cart',{})

        self.assertIn(str(self.product1.id),cart)
        self.assertEqual(cart[str(self.product1.id)],2)