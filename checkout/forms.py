from django import forms
from django.core.exceptions import ValidationError
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'full_name', 'email', 'phone_number',
            'street_address1', 'street_address2',
            'town_or_city', 'postcode', 'country',
            'county',
        )

    def __init__(self, *args, **kwargs):
        """Add placeholders, classes and remove auto labels."""
        super().__init__(*args, **kwargs)

        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True

        for field in self.fields:
            if field != 'country':
                placeholder = f"{placeholders[field]} *" \
                    if self.fields[field].required else placeholders[field]

                self.fields[field].widget.attrs['placeholder'] = placeholder

            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        if phone and len(phone.replace(" ", "").replace("-", "")) < 7:
            raise ValidationError("Phone number seems too short.")
        return phone

    def clean_postcode(self):
        postcode = self.cleaned_data.get("postcode")
        if postcode and len(postcode) < 3:
            raise ValidationError("Postcode must be at least 3 characters.")
        return postcode

    def clean(self):
        """
        Prevent all address fields being blank
        """
        cleaned_data = super().clean()

        addr1 = cleaned_data.get("street_address1")
        town = cleaned_data.get("town_or_city")
        country = cleaned_data.get("country")

        if not addr1 or not town or not country:
            raise ValidationError(
                "Please complete the required address fields."
            )

        return cleaned_data
