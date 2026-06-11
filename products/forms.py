from django import forms
from .models import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        # SKU en lecture seule
        self.fields['sku'].widget.attrs['readonly'] = True
        self.fields['sku'].widget.attrs['class'] = 'form-control text-muted'

        # other customisations
        self.fields['is_available'].label = 'Available for sale'
        self.fields['is_available'].widget.attrs['class'] = 'form-check-input'
        self.fields['description'].widget.attrs.update({
            'rows': 4,
            'placeholder': 'Enter product description here...',
            'class': 'form-control',
        })
