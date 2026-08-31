from django.templatetags.static import static

from milky.email_utils import build_email_font_urls


def build_gift_email_context(
    request, product, customer, contact, personal_message
):
    """Build the email context shared by the send and preview views."""
    return {
        "product": product,
        "customer": customer,
        "contact": contact,
        "personal_message": personal_message,
        "product_image_url": request.build_absolute_uri(
            product.single_image_url or static("images/no-image.png")
        ),
        **build_email_font_urls(request),
    }
