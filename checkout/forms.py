from django import forms
from typing import cast
from .models import Order


class OrderForm(forms.ModelForm):

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

        )

    def __init__(self, *args, **kwargs):
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
        }

        self.fields["delivery_name"].widget.attrs["autofocus"] = True

        for field in self.fields:
            if field in ("delivery_county", "invoice_county"):
                self.fields[field].widget.attrs["class"] = "form-control county-field"
                self.fields[field].widget.attrs["placeholder"] = placeholders[field]
                self.fields[field].label = False  # type: ignore
                continue

            if field in ("delivery_country", "invoice_country"):
                country_field = cast(forms.ChoiceField, self.fields[field])
                country_field.widget.attrs["class"] = "form-control"
                country_field.label = False  # type: ignore
                existing_choices = [
                    (str(code), str(name))
                    for code, name in cast(list[tuple[object, object]], list(country_field.choices))
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
            self.fields[field].label = False  # type: ignore

        # Make invoice fields not required (filled automatically if same as delivery)
        invoice_fields = [
            'invoice_name', 'invoice_surname', 'invoice_phone',
            'invoice_address', 'invoice_city', 'invoice_county',
            'invoice_postcode', 'invoice_country',
        ]
        for field in invoice_fields:
            self.fields[field].required = False  # type: ignore
