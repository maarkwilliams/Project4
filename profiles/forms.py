from django import forms
from django.core.exceptions import ValidationError
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """Add placeholders + Bootstrap classes."""
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
                placeholder = (
                    f"{placeholders.get(field, '')} *"
                    if self.fields[field].required else placeholders.get(field, '')
                )
                self.fields[field].widget.attrs['placeholder'] = placeholder

            self.fields[field].widget.attrs['class'] = (
                'border-black rounded-0 profile-form-input'
            )
            self.fields[field].label = False


    def clean_default_phone_number(self):
        phone = self.cleaned_data.get("default_phone_number")
        if phone and len(phone.replace(" ", "").replace("-", "")) < 7:
            raise ValidationError("Phone number is too short.")
        return phone

    def clean_default_postcode(self):
        postcode = self.cleaned_data.get("default_postcode")
        if postcode and len(postcode) < 3:
            raise ValidationError("Postcode must be at least 3 characters.")
        return postcode

    def clean(self):
        """
        Must provide at least one address field OR leave all blank.
        """
        cleaned = super().clean()

        addr1 = cleaned.get("default_street_address1")
        town = cleaned.get("default_town_or_city")
        country = cleaned.get("default_country")

        if addr1 or town or country:
            if not addr1 or not town or not country:
                raise ValidationError(
                    "If entering address info, you must complete Street Address 1, Town/City and Country."
                )

        return cleaned
