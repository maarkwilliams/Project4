from django import forms
from django.core.exceptions import ValidationError

from .models import UserProfile


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """Add placeholders and Bootstrap classes."""
        super().__init__(*args, **kwargs)

        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True

        for field in self.fields:
            if field != 'default_country':
                base = placeholders.get(field, '')
                placeholder = (
                    f"{base} *" if self.fields[field].required else base
                )
                self.fields[field].widget.attrs['placeholder'] = placeholder

            self.fields[field].widget.attrs['class'] = (
                'border-black rounded-0 profile-form-input'
            )
            self.fields[field].label = False

    def clean_default_phone_number(self):

        phone = self.cleaned_data.get("default_phone_number")
        if phone:
            cleaned = phone.replace(" ", "").replace("-", "")
            if len(cleaned) < 7:
                raise ValidationError("Phone number is too short.")
        return phone

    def clean_default_postcode(self):
        """Ensure postcode has a minimum length."""
        postcode = self.cleaned_data.get("default_postcode")
        if postcode and len(postcode) < 3:
            raise ValidationError(
                "Postcode must be at least 3 characters."
            )
        return postcode

    def clean(self):
        """
        Require full address fields if any address
        information is being entered.
        """
        cleaned = super().clean()

        addr1 = cleaned.get("default_street_address1")
        town = cleaned.get("default_town_or_city")
        country = cleaned.get("default_country")

        address_fields_filled = any([addr1, town, country])

        if address_fields_filled:
            if not all([addr1, town, country]):
                raise ValidationError(
                    "If entering address info, you must complete "
                    "Street Address 1, Town/City and Country."
                )

        return cleaned
