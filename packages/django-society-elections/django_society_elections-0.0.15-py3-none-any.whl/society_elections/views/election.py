from django.http import HttpRequest
from django.shortcuts import render

from ..models import Election
from .helpers import get_latest_election, get_template


def index_view(req: HttpRequest):
    # Get latest election
    election = get_latest_election()
    if election.current_period in (Election.POSTVOTING, Election.FINISHED):
        return render(req, get_template('election_finished'), {
            'election': election
        })

    return render(req, get_template('election_detail'), {
        'election': election,
        'election_period': election.current_period
    })
