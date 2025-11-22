from django.test import TestCase
from django.contrib.auth.models import User
from products.models import Product, Category, Review
from django.core.exceptions import ValidationError


class ProductModelTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Shirts",
            friendly_name="Shirts"
        )

    def test_product_price_cannot_be_negative(self):
        """ Ensure product price validation prevents negative numbers """
        product = Product(
            name="Test Shirt",
            category=self.category,
            price=-10
        )
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_product_rating_average_property(self):
        """ Test average_rating returns correct value """
        user = User.objects.create_user(username="tester", password="pass123")
        product = Product.objects.create(
            name="Test Product",
            category=self.category,
            price=20
        )

        Review.objects.create(product=product, user=user, rating=4)
        Review.objects.create(product=product, user=user, rating=2)

        self.assertEqual(product.average_rating, 3.0)


class ReviewModelTests(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Hats")
        self.user = User.objects.create_user(username="mark", password="pass123")
        self.product = Product.objects.create(
            name="Test Hat",
            category=self.category,
            price=15
        )

    def test_review_rating_must_be_1_to_5(self):
        """ Rating must not exceed validators """
        review = Review(
            product=self.product,
            user=self.user,
            rating=7
        )
        with self.assertRaises(ValidationError):
            review.full_clean()
