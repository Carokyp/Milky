from typing import Any, cast

from allauth.account.forms import LoginForm, SignupForm
from django import forms

from .models import Customer, Contact


def _style_auth_fields(fields):
    """Bootstrap class + an aria-label (allauth ships blank/absent labels)."""
    for name, field in fields.items():
        css = field.widget.attrs.get("class", "")
        field.widget.attrs["class"] = f"{css} form-control".strip()
        aria_label = field.label or field.widget.attrs.get(
            "placeholder"
        ) or name.replace("_", " ").title()
        field.widget.attrs["aria-label"] = aria_label


class MilkyLoginForm(LoginForm):
    """allauth login form with Bootstrap styling + accessible names."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _style_auth_fields(self.fields)


class MilkySignupForm(SignupForm):
    """allauth signup form with Bootstrap styling + accessible names."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _style_auth_fields(self.fields)


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
        for name, field in self.fields.items():
            field.label = False  # type: ignore
            # Placeholders replace the visible label, so expose the same
            # text to assistive tech as an accessible name.
            aria_label = field.widget.attrs.get(
                "placeholder", name.replace("_", " ").title()
            )
            field.widget.attrs["aria-label"] = aria_label

        # Replace blank label on country dropdown
        typed_country_field = cast(Any, self.fields["country"])
        typed_country_field.widget.attrs["aria-label"] = "Country"
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
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Friend's Email",
                }
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
            "address": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Friend's Address",
                }
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
        for name, field in self.fields.items():
            field.label = False  # type: ignore
            aria_label = field.widget.attrs.get(
                "placeholder", name.replace("_", " ").title()
            )
            field.widget.attrs["aria-label"] = aria_label

        # Replace blank label on country dropdown
        typed_country_field = cast(Any, self.fields["country"])
        typed_country_field.widget.attrs["aria-label"] = "Country"
        choices = list(typed_country_field.choices)
        choices[0] = ("", "Country")
        typed_country_field.choices = choices
