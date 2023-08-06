from logging import getLogger

from django.contrib import admin
from django.utils.decorators import method_decorator

from ..models import Position
from .decorators import log_model_admin_action

logger = getLogger(__name__)


@admin.register(Position)
@method_decorator(
    log_model_admin_action('save', Position, logger),
    name='save_model'
)
@method_decorator(
    log_model_admin_action('delete', Position, logger),
    name='delete_model'
)
class PositionAdmin(admin.ModelAdmin):
    """Defines how the Position model is presented on the admin interface
    """
