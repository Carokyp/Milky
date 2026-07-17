from django.templatetags.static import static

from milky.email_utils import build_email_font_urls


def build_confirmation_email_context(request, order, contact_email):
    """Build the template context shared by the real send and the preview view"""
    items = [
        {
            'item': item,
            'image_url': request.build_absolute_uri(
                item.product.product_image.url if item.product.product_image
                else static('images/no_image.png')
            ),
        }
        for item in order.items.all()
    ]
    return {
        'order': order,
        'contact_email': contact_email,
        'items': items,
        **build_email_font_urls(request),
    }
