from django import forms
from django_countries.widgets import CountrySelectWidget
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
        }

        self.fields["delivery_name"].widget.attrs["autofocus"] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f"{placeholders[field]} *"
            else:
                placeholder = placeholders[field]

            self.fields[field].widget.attrs["placeholder"] = placeholder
            self.fields[field].widget.attrs["class"] = "form-control"
            self.fields[field].label = False  # type: ignore

            if field == "delivery_country":
                self.fields[field].widget = CountrySelectWidget(
                    attrs={
                        "class": "form-control country-select",
                        "data-placeholder": placeholder,
                    }
                )
