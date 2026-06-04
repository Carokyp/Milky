from django import forms
from .models import Customer


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
            "county": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "County"}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Phone Number"}
            ),
        }
