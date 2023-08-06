import logging

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from ..forms import NominationForm
from ..models import Candidate, Election, ElectionPosition
from .decorators import validate_election_period
from .helpers import get_latest_election, get_template

logger = logging.getLogger(__name__)


@method_decorator(validate_election_period(Election.NOMINATIONS), 'dispatch')
class NominationFormView(FormView):
    """Sends a NominationForm to the user, and validates the response

    The form is valid if there isn't an existing nomination for this email and 
    position. The user may be required to validate their email.
    """
    form_class = NominationForm

    def get_template_names(self):
        return [get_template('nomination_form'),]

    def get_form(self, *args, **kwargs):
        form: NominationForm = super().get_form(*args, **kwargs)
        form.fields['position'].choices = [
            (position.pk, str(position)) for position
            in ElectionPosition.objects.filter(
                election=get_latest_election()
            )
        ]
        return form

    def form_valid(self, form: NominationForm):
        candidate: Candidate = form.save()
        candidate.send_verification_email()
        logger.info(
            f'{candidate.full_name} was nominated for {candidate.position}'
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['election'] = get_latest_election()
        return context_data

    def get_success_url(self) -> str:
        return reverse('society_elections:nomination_success')


@method_decorator(validate_election_period(Election.NOMINATIONS), 'dispatch')
class NominationSuccessView(TemplateView):
    """When a nomination has been successful"""

    def get_template_names(self):
        return [get_template('nomination_success'),]


@validate_election_period(Election.NOMINATIONS)
def verify_candidate_view(req: HttpRequest) -> HttpResponse:
    """Verify a given UUID belongs to a candidate
    
    Verifies that the given UUID belongs to a candidate in an election, and 
    verify their email in the database

    Args:
        req (HttpRequest): Request sent to verify the email

    Returns:
        HttpResponse
    """
    uuid = req.GET.get('uuid').lower()
    matching_candidates = Candidate.objects.filter(email_uuid=uuid)
    if not matching_candidates.exists():
        logger.warning(
            f'Someone tried to verify a candidate with UUID="{uuid}", but no '
            'such UUID existed in the database'
        )   
        return render(req, get_template('candidate_verify'), {
            'verified': False
        })

    candidate: Candidate
    for candidate in matching_candidates:
        logger.info(f'Verifying candidate email {candidate.email}')
        candidate.email_verified = True
        candidate.save()
    return render(req, get_template('candidate_verify'), {
        'verified': True
    })
