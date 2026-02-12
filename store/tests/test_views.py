from django.test import TestCase
from django.urls import reverse
from store.models import Category, Product

class ProductViewsTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Tea")
        self.product = Product.objects.create(
            name = "Green Tea",
            price = 259,
            category = self.category
        )

    def test_product_list_view_status_code(self):
        url = reverse("product_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)

    def test_product_list_view_contains_product(self):
        url = reverse("product_list")
        response = self.client.get(url)
        self.assertContains(response,"Green Tea")