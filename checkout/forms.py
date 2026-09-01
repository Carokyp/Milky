from typing import Iterable, cast

from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    """Form for collecting delivery and invoice details at checkout."""

    class Meta:
        model = Order
        fields = (
            "delivery_name",
            "delivery_surname",
            "delivery_phone",
            "delivery_address",
            "delivery_city",
            "delivery_county",
            "delivery_postcode",
            "delivery_country",
            "invoice_name",
            "invoice_surname",
            "invoice_phone",
            "invoice_address",
            "invoice_city",
            "invoice_county",
            "invoice_postcode",
            "invoice_country",
            "email",
        )

    def __init__(self, *args, **kwargs):
        """Style fields, add placeholders, and toggle required fields."""
        user_authenticated = kwargs.pop("user_authenticated", False)
        super().__init__(*args, **kwargs)

        placeholders = {
            "delivery_name": "Name",
            "delivery_surname": "Surname",
            "delivery_phone": "Phone Number",
            "delivery_address": "Street Address",
            "delivery_city": "City",
            "delivery_county": "County",
            "delivery_postcode": "Postal Code",
            "delivery_country": "Country",
            "invoice_name": "Name",
            "invoice_surname": "Surname",
            "invoice_phone": "Phone Number",
            "invoice_address": "Street Address",
            "invoice_city": "City",
            "invoice_county": "County",
            "invoice_postcode": "Postal Code",
            "invoice_country": "Country",
            "email": "Email Address",
        }

        # Make email not required if user is authenticated
        if user_authenticated:
            self.fields["email"].required = False

        # Prefix so screen readers can tell the delivery block from the
        # invoice block when the visible labels are hidden.
        aria_prefixes = {"delivery": "Delivery", "invoice": "Invoice"}

        for field in self.fields:
            aria_prefix = aria_prefixes.get(field.split("_")[0], "")
            aria_label = f"{aria_prefix} {placeholders[field]}".strip()

            if field in ("delivery_county", "invoice_county"):
                self.fields[field].widget.attrs[
                    "class"
                ] = "form-control county-field"
                self.fields[field].widget.attrs["placeholder"] = placeholders[
                    field
                ]
                self.fields[field].widget.attrs["aria-label"] = aria_label
                self.fields[field].label = False  # type: ignore
                continue

            if field in ("delivery_country", "invoice_country"):
                country_field = cast(forms.ChoiceField, self.fields[field])
                country_field.widget.attrs["class"] = "form-control"
                country_field.widget.attrs["aria-label"] = aria_label
                country_field.label = False  # type: ignore
                choices_iterable = cast(
                    Iterable[tuple[object, object]], country_field.choices
                )
                existing_choices = [
                    (str(code), str(name))
                    for code, name in choices_iterable
                    if code
                ]
                country_field.choices = [("", "Country *"), *existing_choices]
                continue

            if self.fields[field].required:
                placeholder = f"{placeholders[field]} *"
            else:
                placeholder = placeholders[field]

            self.fields[field].widget.attrs["placeholder"] = placeholder
            self.fields[field].widget.attrs["class"] = "form-control"
            self.fields[field].widget.attrs["aria-label"] = aria_label
            self.fields[field].label = False  # type: ignore

        # Invoice fields are optional: filled automatically when the
        # "same as delivery" checkbox is used.
        invoice_fields = [
            "invoice_name",
            "invoice_surname",
            "invoice_phone",
            "invoice_address",
            "invoice_city",
            "invoice_county",
            "invoice_postcode",
            "invoice_country",
        ]
        for field in invoice_fields:
            self.fields[field].required = False  # type: ignore
