from django import forms
from .models import Customer, Contact


class CustomerForm(forms.ModelForm):
    """Form for creating and updating Customer instances."""

    class Meta:
        model = Customer
        fields = [
            "name",
            "surname",
            "display_name",
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
            "display_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Username"}
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label = False  # type: ignore

        # Replace blank label on country dropdown
        choices = list(self.fields["country"].choices)
        choices[0] = ("", "Country")
        self.fields["country"].choices = choices


class GiftACanForm(forms.ModelForm):
    """Form for gifting a can to a friend."""
    class Meta:

        model = Contact
        fields = [
            "email",
            "name",
            "surname",
            "phone_number",
        ]

        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Friend's Email"}
            ),
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Name"}
            ),
            "surname": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Surname"}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Phone Number"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label = False  # type: ignore
