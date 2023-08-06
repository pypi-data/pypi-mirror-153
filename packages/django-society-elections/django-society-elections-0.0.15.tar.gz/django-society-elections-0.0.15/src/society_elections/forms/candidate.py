from logging import getLogger

from django.core.exceptions import ValidationError
from django.forms import ModelForm

from ..models import Candidate, Election, ElectionPosition

logger = getLogger(__name__)

class BaseCandidateForm(ModelForm):
    """Base form for a Candidate providing validation

    Should not be used directly, but should be subclassed for different purposes
    """

    def clean(self):
        """Validate the email given meets whitelisting of election"""
        cleaned_data = super().clean()

        email: str = cleaned_data.get('email')
        position: ElectionPosition = cleaned_data.get('position')
        election: Election = position.election

        logger.debug(
            f'Verifying that "{email}" has a valid domain in the whitelist'
        )

        email_whitelist = election.candidate_email_domain_whitelist.split()
        logger.debug(f'Whitelist: {email_whitelist}')
        email_domain = email.split('@')[1]
        logger.debug(f'Email domain to validate: {email_domain}')
        if email_domain not in email_whitelist:
            logger.debug(f'Email "{email}" not in valid domains')
            self.add_error('email', ValidationError(
                'Email not in whitelisted domains for this election'
            ))
        
        return cleaned_data


class CandidateAdminForm(BaseCandidateForm):
    """Form for a CandidateModel in the admin interface
    """
    class Meta:
        model = Candidate
        exclude = ()


class NominationForm(BaseCandidateForm):
    """Form for a new candidate
    
    Subclasses the base form, but only includes specific fields
    """
    class Meta:
        model = Candidate
        fields = (
            'full_name',
            'email',
            'position',
            'manifesto'
        )