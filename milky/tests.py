"""Project-level tests for the develop branch's settings.

The develop branch carries a developer-oriented settings.py that differs
from main's production configuration (see the Deployment section of the
README). These tests pin the differences that develop is expected to add.

Run with:  python manage.py test milky
"""
from django.conf import settings
from django.test import SimpleTestCase


class DevelopmentConfigTests(SimpleTestCase):
    """Assertions about the develop branch's settings.py."""

    def test_console_logging_handler_is_configured(self):
        # develop streams logs to the console so problems are visible
        # during `runserver`. main does not define LOGGING at all.
        handlers = getattr(settings, "LOGGING", {}).get("handlers", {})
        self.assertIn("console", handlers)
        self.assertEqual(
            handlers["console"]["class"], "logging.StreamHandler"
        )

    def test_django_logs_at_debug_level_on_develop(self):
        logging_config = getattr(settings, "LOGGING", {})
        django_logger = logging_config.get("loggers", {}).get("django", {})
        self.assertEqual(django_logger.get("level"), "DEBUG")
