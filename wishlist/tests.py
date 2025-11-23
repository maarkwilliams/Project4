from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from products.models import Product, Category
from wishlist.models import Wishlist, WishlistItem


class WishlistViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="mark",
            password="pass123",
        )
        self.client.login(username="mark", password="pass123")

        self.category = Category.objects.create(name="Tops")
        self.product = Product.objects.create(
            name="Basic Tee",
            category=self.category,
            price=12,
        )

        self.wishlist, _ = Wishlist.objects.get_or_create(user=self.user)

    def test_wishlist_page_loads(self):
        response = self.client.get(reverse("wishlist"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wishlist/wishlist.html")

    def test_add_to_wishlist(self):
        response = self.client.get(
            reverse("add_to_wishlist", args=[self.product.id]),
        )
        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            WishlistItem.objects.filter(
                wishlist=self.wishlist,
                product=self.product,
            ).exists()
        )

    def test_remove_from_wishlist(self):
        WishlistItem.objects.create(
            wishlist=self.wishlist,
            product=self.product,
        )

        response = self.client.get(
            reverse("remove_from_wishlist", args=[self.product.id]),
        )
        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            WishlistItem.objects.filter(
                wishlist=self.wishlist,
                product=self.product,
            ).exists()
        )


class WishlistModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="john",
            password="pass123",
        )
        self.wishlist, _ = Wishlist.objects.get_or_create(user=self.user)

        category = Category.objects.create(name="Shoes")
        self.product = Product.objects.create(
            name="Boots",
            category=category,
            price=50,
        )

    def test_wishlist_item_creation(self):
        item = WishlistItem.objects.create(
            wishlist=self.wishlist,
            product=self.product,
        )

        self.assertEqual(item.wishlist.user.username, "john")
        self.assertEqual(item.product.name, "Boots")
