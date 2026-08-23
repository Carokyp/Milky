import os

from django.forms.widgets import ClearableFileInput


class CustomClearableFileInput(ClearableFileInput):
    """File input widget showing the current file's name, clearable."""

    clear_checkbox_label = 'Remove Image'
    initial_text = 'Current Image'
    input_text = ''
    template_name = (
        'products/custom_widget_templates/custom_clearable_file_input.html'
    )

    def get_context(self, name, value, attrs):
        """Add the current file's basename to the widget context."""
        context = super().get_context(name, value, attrs)
        if value:
            context['widget']['filename'] = os.path.basename(value.name)
        return context
