import logging

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from ipware.ip import get_client_ip

from .. import app_settings
from ..forms import RegisteredVoterForm
from ..models import AnonymousVoter, Election, RegisteredVoter
from .decorators import validate_election_period
from .helpers import get_latest_election, get_template

logger = logging.getLogger(__name__)


@validate_election_period(Election.VOTING)
def create_voter_view(req: HttpRequest) -> HttpResponse:
    """Validates the VoterForm and creates a new voter in the DB

    Args:
        req (HttpRequest): Request made by user

    Returns:
        HttpResponse: Response to user

    Raises:
        Http404: No election currently running
    """
    election = get_latest_election()
    if req.method == 'POST':
        form = RegisteredVoterForm(req.POST)
        if form.is_valid():
            logger.debug(
                f'Checking if voter "{form.cleaned_data["email"]}" has already '
                'registered'
                )
            existing_voter = RegisteredVoter.objects.filter(
                election=election, email=form.cleaned_data['email']
            )
            if existing_voter.exists():
                logger.debug(
                    f'Voter "{existing_voter[0].email}" found for this election'
                )
                return render(req, get_template('voter_exists'), {
                    'election': election,
                    'voter': existing_voter.get()
                })
            else:
                # Verify email in correct domain
                email_domain = form.cleaned_data['email'].split('@')[1]
                domains = election.voter_email_domain_whitelist.split()
                logger.debug(
                    f'Verifying email {form.cleaned_data["email"]} has a valid '
                    f'domain in {domains}'
                )
                if email_domain not in domains:
                    logger.debug(f'"{email_domain}" not in {domains}')
                    form.add_error('email', ValidationError(
                        'Email domain not valid for this election'
                    ))
                else:
                    # Save and send email
                    logger.debug(f'Email {form.cleaned_data["email"]} valid!')
                    voter: RegisteredVoter = form.save(commit=False)
                    voter.election = election
                    voter.save()
                    voter.send_verification_email()
                    return render(
                        req, get_template('voter_verification_sent'), {
                            'election': election,
                            'voter': voter
                        }
                    )
    else:
        form = RegisteredVoterForm()
    return render(req, get_template('voter_form'), {
        'election': election,
        'form': form
    })


@validate_election_period(Election.VOTING)
def verify_voter_view(req: HttpRequest) -> HttpResponse:
    """Verify a voter using the GET data in the request

    Args:
        req (HttpRequest): Request from user

    Raises:
        Http404: Voter does not exist

    Returns:
        HttpResponse: response to user
    """
    uuid = req.GET.get('uuid').lower()
    election = get_latest_election()
    ip = get_client_ip(req)
    try:
        voter = get_object_or_404(RegisteredVoter, pk=uuid, election=election)
    except Http404:
        logger.info(f'Voter 404 not found: {uuid} "{election}" ({ip})')
        return render(req, get_template('voter_404'), {
            'uuid': uuid
        })
    if not voter.verified:
        logger.debug(f'Voter {uuid} not verified yet, verifying...')
        voter.verified_at = timezone.now()
        voter.save()
        logger.debug(f'Voter {uuid} verified')
        if voter.election.anonymous:
            # Create anonymous user with password and return password to user
            logger.debug(
                'Anonymous election detected, creating anonymous voter'
            )
            password = AnonymousVoter.generate_voter_password()
            anon_voter = AnonymousVoter()
            anon_voter.election = voter.election
            anon_voter.password = AnonymousVoter.hash_password(password)
            anon_voter.save()
            logger.debug('Anonymous voter created, emailing password to user')
            message = f'''<p>You have successfully verified your email to vote in the election "{voter.election}"". Your password to vote is shown below. Keep it safe and confidential as it identifies you as a voter.<p>
            <p><b>{password}<b><p>
            <p><a href="{app_settings.ROOT_URL}{reverse('society_elections:vote')}">Click here</a> to vote, or copy and paste the following link into your browser: <code>{app_settings.ROOT_URL}{reverse('society_elections:vote')}</code></p>
            '''
            send_mail(
                subject=f'Voting password for election {voter.election}',
                message=message,
                from_email=None,
                recipient_list=[voter.email,],
                html_message=message
            )
            logger.debug('Password email sent, returning template')
            return render(req, get_template('voter_verified_anon_election'), {
                'password': password,
                'election': election
            })
        else:
            messages.add_message(req, messages.INFO, 
                'Your email has successfully been verified.'
            )
    elif voter.election.anonymous:
        # If voter in anonymous election already verified, do not generate 
        # another password
        logger.warning(
            'Verified voter requested re-verification in anon election: '
            f'{voter} "{election}" ({ip})'
        )
        return render(req, get_template('voter_exists'), {
            'voter': voter,
            'election': election
        })
    
    # Voter has been verified
    return redirect(reverse('society_elections:vote') + f'?uuid={uuid}')


@require_POST
@validate_election_period(Election.VOTING)
def resend_voter_verification(req: HttpRequest) -> HttpResponse:
    """Resends the verification email for a given RegisteredVoter
    
    This view will not resend the verification email for a verified voter in an 
    anonymous election as this would not resolve any issues. The user would 
    click the verification email and be told that they have already been 
    verified.
    
    Args:
        req (HttpRequest): Request from user
        
    Returns:
        HttpResponse: Response to user
    """
    election = get_latest_election()
    email = req.POST.get('email')
    uuid = req.POST.get('uuid')
    ip = get_client_ip(req)

    if email is not None and uuid is not None:
        return HttpResponse(content='400 Bad request', status=400)

    # Find Voter
    try:
        if email is not None:
            voter = get_object_or_404(
                RegisteredVoter, email=email, election=election
            )
        else:
            voter = get_object_or_404(
                RegisteredVoter, pk=uuid, election=election
            )
    except Http404:
        logger.info(f'Voter 404 not found: {email} "{election}" ({ip})')
        return render(req, get_template('voter_404'), {
            'email': email
        })
    
    # Check for bad conditions
    if election.anonymous and voter.verified:
        logger.info(
            'Verified voter requested re-verification in anon election: '
            f'{voter} "{election}" ({ip})'
        )
        return render(req, get_template('voter_exists'), {
            'voter': voter,
            'election': election
        })
    
    # Resend verification email
    voter.send_verification_email()
    return render(req, get_template('voter_verification_sent'), {
            'election': election,
            'voter': voter
    })
    