from django.urls import path

from society_elections.views.vote import delete_vote_ajax

from .views import (NominationFormView, NominationSuccessView,
                    VoteSubmittedView, create_vote_ajax, create_voter_view,
                    delete_vote_ajax, index_view, resend_voter_verification,
                    verify_candidate_view, verify_voter_view, vote_view)

app_name = 'society_elections'
urlpatterns = [
    # Nominations
    path('nominate/', NominationFormView.as_view(), name='nomination_create'),
    path('nominate/success/', NominationSuccessView.as_view(), 
        name='nomination_success'
    ),
    path('nominate/verify/', verify_candidate_view, name='candidate_verify'),
    # Voters
    path('vote/register/', create_voter_view, name='voter_create'),
    path('vote/verify/', verify_voter_view, name='voter_verify'),
    path(
        'vote/register/resend-verification/', 
        resend_voter_verification, 
        name='voter_resend_verification'
    ),
    # Voting
    path('vote/', vote_view, name='vote'),
    path('vote/submitted', VoteSubmittedView.as_view(), name='vote_submitted'),
    path(
        'vote/ajax/create', create_vote_ajax, name='vote_create'
    ),
    path(
        'vote/ajax/delete', delete_vote_ajax, name='vote_delete'
    ),
    # Elections
    path('', index_view, name='index')
]
