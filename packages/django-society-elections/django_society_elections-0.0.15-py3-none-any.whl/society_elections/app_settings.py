"""Defines the settings for this package"""
from django.conf import settings

TEMPLATE_PREFIX = getattr(
    settings, 'SOCIETY_ELECTIONS_TEMPLATE_PREFIX', 'society_elections/'
)
ROOT_URL = getattr(
    settings, 'SOCIETY_ELECTIONS_ROOT_URL', 'http://localhost:8000'
)