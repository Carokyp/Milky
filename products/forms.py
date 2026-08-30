from django import forms

from .models import Product, Review
from .widgets import CustomClearableFileInput


class ProductForm(forms.ModelForm):
    """Form for creating and editing products."""

    product_image = forms.ImageField(
        label="Image", required=False, widget=CustomClearableFileInput()
    )
    background_image = forms.ImageField(
        required=False, widget=CustomClearableFileInput()
    )
    objects_image = forms.ImageField(
        required=False, widget=CustomClearableFileInput()
    )
    can_image = forms.ImageField(
        required=False, widget=CustomClearableFileInput()
    )

    class Meta:
        model = Product
        fields = "__all__"

    # Per-field label / help_text / extra widget attributes, applied in
    # __init__ so each field is only touched if it actually exists on
    # the form (fields = '__all__' means the model drives the list).
    FIELD_CUSTOMIZATIONS = {
        "sku": {
            "widget_attrs": {
                "readonly": True,
                "class": "form-control text-muted",
            },
        },
        "is_available": {
            "label": "Available for sale",
            "widget_attrs": {"class": "form-check-input"},
        },
        "featured": {
            "widget_attrs": {"class": "form-check-input"},
        },
        "background_image": {
            "label": "Card background",
            "help_text": ("Background that fills the product card."),
        },
        "objects_image": {
            "label": "Floating elements",
            "help_text": (
                "Decorative elements floating around (transparent PNG)."
            ),
        },
        "can_image": {
            "label": "Can photo",
            "help_text": "Product can (transparent PNG).",
        },
        "product_image_url": {
            "help_text": ("Use a direct link to an image (https://…)."),
        },
        "description": {
            "widget_attrs": {
                "rows": 3,
                "placeholder": "Enter product description here...",
                "class": "form-control",
            },
        },
    }

    def __init__(self, *args, **kwargs):
        """Apply Bootstrap classes and field-specific customisations."""
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

        for name, options in self.FIELD_CUSTOMIZATIONS.items():
            if name not in self.fields:
                continue
            field = self.fields[name]
            if "label" in options:
                field.label = options["label"]
            if "help_text" in options:
                field.help_text = options["help_text"]
            if "widget_attrs" in options:
                field.widget.attrs.update(options["widget_attrs"])


class ReviewForm(forms.ModelForm):
    """Form for submitting a product review."""

    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.NumberInput(
                attrs={"class": "form-control", "min": 1, "max": 5}
            ),
            "comment": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
        }
