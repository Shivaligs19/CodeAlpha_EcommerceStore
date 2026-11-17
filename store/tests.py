from django.test import TestCase
from .models import Product


class HomePageTests(TestCase):
    def test_homepage_renders_complete_product_catalog(self):
        Product.objects.create(
            name='Apple',
            category='Fruit',
            description='Fresh apple',
            price='1.25',
            stock=5,
        )

        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<!DOCTYPE html>')
        self.assertContains(response, '</html>')
        self.assertContains(response, 'Apple')
        self.assertContains(response, 'data-category="fruit"')
        self.assertContains(response, 'Add to Cart')
