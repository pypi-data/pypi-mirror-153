import csv
from io import StringIO
from logging import getLogger

from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import ngettext

from ..forms import ElectionForm
from ..models import Election, ElectionPosition, Vote
from .decorators import log_model_admin_action

logger = getLogger(__name__)


@admin.register(Election)
@method_decorator(
    log_model_admin_action('save', Election, logger),
    name='save_model'
)
@method_decorator(
    log_model_admin_action('delete', Election, logger),
    name='delete_model'
)
class ElectionAdmin(admin.ModelAdmin):
    """Class defining how an Election model is presented in the admin interface

    Attributes:
        list_display (tuple): Which fields should be shown in the table
        form (django.forms.ModelForm): Which form to use for the model
    """
    list_display = (
        'admin_title', 'nominations_start', 'voting_start', 'ended_at'
    )
    form = ElectionForm
    actions = ['end_election', 'download_csv_of_votes']


    @admin.action(description='End election')
    @method_decorator(log_model_admin_action(
        'end election', Election, logger
    ))
    def end_election(
        self, request: HttpRequest, queryset: QuerySet
    ):
        """Marks a given set of elections as finished

        Args:
            request (HttpRequest): Request from staff user
            queryset (QuerySet): Queryset of elections to finish
        """
        queryset.update(
            ended_at=timezone.now(),
            ended_by=request.user
        )
        messages.add_message(request, messages.SUCCESS,
            f'Successfully ended {queryset.count()} election'+
            ngettext('', 's', queryset.count())
        )


    @admin.action(description='Download CSV of votes')
    @method_decorator(log_model_admin_action(
        'download csv of votes', Election, logger
    ))
    def download_csv_of_votes(
        self, request: HttpRequest, queryset: QuerySet
    ):
        """Download a CSV of all votes cast in the election

        Args:
            request (HttpRequest): Request from a staff user
            queryset (QuerySet): Queryset of the elections to fetch votes for
        """
        f = StringIO()
        writer = csv.writer(f)
        writer.writerow([
            'voter_id', 'election_id', 'election_admin_title', 'anonymous',
            'position', 'candidate', 'candidate_id',
            'vote_cast_at', 'vote_last_modified'
        ])
        election: Election
        position: ElectionPosition
        vote: Vote
        for election in queryset:
            for position in election.positions.all():
                for vote in position.votes.all():
                    writer.writerow([
                        vote.voter_pk,
                        str(election.pk),
                        election.admin_title, 
                        election.anonymous,
                        position.position.title,
                        vote.candidate.full_name,
                        str(vote.candidate.pk),
                        vote.vote_cast_at.isoformat(),
                        vote.vote_last_modified_at.isoformat()
                    ])
        f.seek(0)
        response = HttpResponse(f, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=votes.csv'
        return response


    def save_model(self, request: HttpRequest, obj: Election, *args, **kwargs):
        """Set request-specific data on the object before saving to database

        Args:
            request (HttpRequest): Request made when saving model
            obj (Election): Election object to save in database
        """
        if obj.pk is None:
            obj.created_by = request.user
        super().save_model(request, obj, *args, **kwargs)

