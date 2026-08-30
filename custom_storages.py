# From the Code Institute "Boutique Ado" walkthrough (S3 storage classes).
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """Store collected static files under the bucket's static/ prefix."""

    location = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):
    """Store uploaded media files under the bucket's media/ prefix."""

    location = settings.MEDIAFILES_LOCATION
