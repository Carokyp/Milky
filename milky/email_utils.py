from django.templatetags.static import static


def build_email_font_urls(request):
    """Return absolute URLs for the self-hosted fonts used by emails.

    Used by templates/emails/_email_styles.css and shared by every app
    that sends a styled HTML email (checkout, products...).
    """
    return {
        'font_bebas_url': request.build_absolute_uri(
            static('fonts/bebas-neue-regular.woff2')
        ),
        'font_poppins_regular_url': request.build_absolute_uri(
            static('fonts/poppins-regular.woff2')
        ),
        'font_poppins_bold_url': request.build_absolute_uri(
            static('fonts/poppins-bold.woff2')
        ),
    }
