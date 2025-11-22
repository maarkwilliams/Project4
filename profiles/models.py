from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_countries.fields import CountryField
from django.core.validators import RegexValidator


phone_validator = RegexValidator(
    regex=r'^\+?[\d\s\-]{7,15}$',
    message="Enter a valid phone number (7–15 digits, spaces or dashes allowed)."
)

postcode_validator = RegexValidator(
    regex=r'^[A-Za-z0-9\s\-]{3,10}$',
    message="Enter a valid postcode (3–10 letters/numbers)."
)


class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    default_phone_number = models.CharField(
        max_length=20, null=True, blank=True,
        validators=[phone_validator]
    )
    default_street_address1 = models.CharField(
        max_length=80, null=True, blank=True
    )
    default_street_address2 = models.CharField(
        max_length=80, null=True, blank=True
    )
    default_town_or_city = models.CharField(
        max_length=40, null=True, blank=True
    )
    default_county = models.CharField(
        max_length=80, null=True, blank=True
    )
    default_postcode = models.CharField(
        max_length=20, null=True, blank=True,
        validators=[postcode_validator]
    )
    default_country = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        choices=[('', 'Select Country')] + list(CountryField().choices),
        default=''
    )

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()
