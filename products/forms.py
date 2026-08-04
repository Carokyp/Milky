from django import forms
from .models import Product
from .models import Review
from .widgets import CustomClearableFileInput


class ProductForm(forms.ModelForm):
    product_image = forms.ImageField(
        label='Image', required=False, widget=CustomClearableFileInput()
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
        if 'featured' in self.fields:
            self.fields['featured'].widget.attrs['class'] = 'form-check-input'
        if 'background_image' in self.fields:
            self.fields['background_image'].label = 'Card background'
            self.fields['background_image'].help_text = 'Background that fills the product card.'
        if 'objects_image' in self.fields:
            self.fields['objects_image'].label = 'Floating elements'
            self.fields['objects_image'].help_text = 'Decorative elements floating around (transparent PNG).'
        if 'can_image' in self.fields:
            self.fields['can_image'].label = 'Can photo'
            self.fields['can_image'].help_text = 'Product can (transparent PNG).'
        if 'description' in self.fields:
            self.fields['description'].widget.attrs.update({
                'rows': 4,
                'placeholder': 'Enter product description here...',
                'class': 'form-control',
            })


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
