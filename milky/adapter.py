from allauth.core import context as allauth_context
from allauth.account.adapter import DefaultAccountAdapter

from milky.email_utils import build_email_font_urls


class CustomAccountAdapter(DefaultAccountAdapter):
    """Adds the shared email font URLs to every allauth email's context.

    Needed so templates/allauth/account/email/*_message.html can reuse
    templates/emails/_email_styles.css like the checkout and gift emails do.
    """

    def send_mail(self, template_prefix, email, context):
        """Merge the shared email font URLs into the context, then send."""
        request = allauth_context.request
        if request is not None:
            context = {**context, **build_email_font_urls(request)}
        super().send_mail(template_prefix, email, context)
