from django import forms
from .models import Product
from .widgets import CustomClearableFileInput


class ProductForm(forms.ModelForm):
    product_image = forms.ImageField(
        label='Image',
        required=False,
        widget=CustomClearableFileInput()
    )

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        # SKU field should be read-only in the form
        if 'sku' in self.fields:
            self.fields['sku'].widget.attrs['readonly'] = True
            self.fields['sku'].widget.attrs['class'] = 'form-control text-muted'

        # other customisations
        if 'is_available' in self.fields:
            self.fields['is_available'].label = 'Available for sale'
            self.fields['is_available'].widget.attrs['class'] = 'form-check-input'
        if 'description' in self.fields:
            self.fields['description'].widget.attrs.update({
                'rows': 4,
                'placeholder': 'Enter product description here...',
                'class': 'form-control',
            })
