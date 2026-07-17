from django.templatetags.static import static

from milky.email_utils import build_email_font_urls


def build_gift_email_context(request, product, customer, contact, personal_message):
    """Build the template context shared by the real send and the preview view"""
    return {
        'product': product,
        'customer': customer,
        'contact': contact,
        'personal_message': personal_message,
        'product_image_url': request.build_absolute_uri(
            product.product_image.url if product.product_image
            else static('images/no_image.png')
        ),
        **build_email_font_urls(request),
    }
