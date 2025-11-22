from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.utils import timezone

class RecentlyViewed(models.Model):
    """
    Stores products recently viewed by each user.
    Each combination of user + product is unique.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recent_views")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-timestamp"]
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user.username} viewed {self.product.name}"
