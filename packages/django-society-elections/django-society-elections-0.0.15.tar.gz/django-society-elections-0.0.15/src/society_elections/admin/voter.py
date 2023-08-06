from logging import getLogger

from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.decorators import method_decorator
from django.utils.translation import ngettext

from ..models import RegisteredVoter
from .decorators import log_model_admin_action

logger = getLogger(__name__)

@admin.register(RegisteredVoter)
@method_decorator(
    log_model_admin_action('save', RegisteredVoter, logger),
    name='save_model'
)
@method_decorator(
    log_model_admin_action('delete', RegisteredVoter, logger),
    name='delete_model'
)
class RegisteredVoterAdmin(admin.ModelAdmin):
    """Class defining how a registered voter appears on the admin interface

    Attributes:
        list_display (tuple): How registered voters are grouped by date
        actions (list): Actions available to perform on the models in the admin 
            interface
    """
    list_display = ('email', 'election', 'verified', 'registered_at')
    actions = ['resend_verification_email_action']

    @admin.action(description='Resend verification emails')
    @method_decorator(log_model_admin_action(
        'resend verification email', RegisteredVoter, logger
    ))
    def resend_verification_email_action(
        self, request: HttpRequest,  queryset: QuerySet
    ):
        """Set request-specific data on the object before saving to database

        Args:
            request (HttpRequest): Request made when saving model
            obj (Election): Election object to save in database
        """
        voter: RegisteredVoter
        for voter in queryset:
            voter.send_verification_email()
        messages.add_message(request, messages.SUCCESS,
            f'Successfully sent {queryset.count()} verification email'+
            ngettext('', 's', queryset.count())
        )
