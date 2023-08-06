from logging import getLogger

from django.contrib import admin
from django.forms import ModelForm
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.http.response import Http404

from ..models import ElectionPosition, Candidate
from .decorators import log_model_admin_action

logger = getLogger(__name__)


@admin.register(ElectionPosition)
@method_decorator(
    log_model_admin_action('save', ElectionPosition, logger),
    name='save_model'
)
@method_decorator(
    log_model_admin_action('delete', ElectionPosition, logger),
    name='delete_model'
)
class ElectionPositionAdmin(admin.ModelAdmin):
    """Defines how the ElectionPosition model is presented on the admin 
    interface
    """
    def save_ron(self, position: ElectionPosition):
        try:
            existing_ron = get_object_or_404(
                Candidate, position=position, email="RON@example.com"
            )
        except Http404:
            if position.allow_ron:
                logger.debug('RON allowed, creating...')
                new_ron = Candidate(
                    position=position,
                    full_name='RON',
                    email='RON@example.com',
                    manifesto='Re-open nominations',
                    email_verified=True
                )
                new_ron.save()
        else:
            logger.debug('Existing RON found')
            if not position.allow_ron:
                logger.debug('RON not allowed. Deleting...')
                existing_ron.delete()


    def save_abstain(self, position: ElectionPosition):
        try:
            existing_abstain = get_object_or_404(
                Candidate, position=position, email="abstain@example.com"
            )
        except Http404:
            if position.allow_abstain:
                logger.debug('Abstain allowed, creating...')
                new_abstain = Candidate(
                    position=position,
                    full_name='Abstain',
                    email='abstain@example.com',
                    manifesto='Abstain from voting for this position',
                    email_verified=True
                )
                new_abstain.save()
        else:
            logger.debug('Existing abstain found')
            if not position.allow_abstain:
                logger.debug('Abstain not allowed. Deleting...')
                existing_abstain.delete()


    def save_model(
        self, 
        request: HttpRequest, 
        obj: ElectionPosition, 
        form: ModelForm, 
        change: bool
    ) -> None:
        """Create/Delete RON and Abstain Candidates based on allow_ron and
        allow_abstain

        Args:
            request (HttpRequest): Request that was made
            obj (ElectionPosition): ElectionPosition to examine
            form (ModelForm): Form submission
            change (bool): Whether or not an existing object is being updated
        """
        super().save_model(request, obj, form, change)
        obj.refresh_from_db()
        self.save_ron(obj)
        self.save_abstain(obj)

