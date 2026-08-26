from typing import Any, cast

from django import forms

from .models import Customer, Contact


class CustomerForm(forms.ModelForm):
    """Form for creating and updating Customer instances."""

    class Meta:
        model = Customer
        fields = [
            "name",
            "surname",
            "address",
            "postal_code",
            "city",
            "country",
            "phone_number",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Name"}
            ),
            "surname": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Surname"}
            ),
            "address": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Address"}
            ),
            "postal_code": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Postal Code"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "City"}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Phone Number"}
            ),
        }

    def __init__(self, *args, **kwargs):
        """Style all fields and give the country dropdown a placeholder."""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label = False  # type: ignore

        # Replace blank label on country dropdown
        typed_country_field = cast(Any, self.fields["country"])
        choices = list(typed_country_field.choices)
        choices[0] = ("", "Country")
        typed_country_field.choices = choices


class GiftACanForm(forms.ModelForm):
    """Form for gifting a can to a friend."""

    class Meta:
        model = Contact
        fields = [
            "email",
            "name",
            "surname",
            "phone_number",
            "address",
            "postal_code",
            "city",
            "country",
        ]

        widgets = {
            "email": forms.EmailInput(attrs={
                "class": "form-control", "placeholder": "Friend's Email"
            }),
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Name"}
            ),
            "surname": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Surname"}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Phone Number"}
            ),
            "address": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Friend's Address"}
            ),
            "postal_code": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Postal Code"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "City"}
            ),
        }

    def __init__(self, *args, **kwargs):
        """Remove field labels so placeholders act as labels instead."""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label = False  # type: ignore

        # Replace blank label on country dropdown
        typed_country_field = cast(Any, self.fields["country"])
        choices = list(typed_country_field.choices)
        choices[0] = ("", "Country")
        typed_country_field.choices = choices
