from django.templatetags.static import static


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
        'font_bebas_url': request.build_absolute_uri(static('fonts/bebas-neue-regular.woff2')),
        'font_poppins_regular_url': request.build_absolute_uri(static('fonts/poppins-regular.woff2')),
        'font_poppins_bold_url': request.build_absolute_uri(static('fonts/poppins-bold.woff2')),
    }
