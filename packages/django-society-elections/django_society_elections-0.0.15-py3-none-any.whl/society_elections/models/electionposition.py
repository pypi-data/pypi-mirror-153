from django.db import models

from ..apps import SocietyElectionsConfig
from .election import Election
from .position import Position


class ElectionPosition(models.Model):
    """Specifies a position to allow candidates to run for in a given election

    Essentially implements a many-to-many relation, with some additional fields

    Attributes:
        position (Position): The position to include
        election (Election): Election the position is to be included in
        candidate_required (bool): Whether or not this position requires a 
            candidate in order for a successful election to take place
        allow_ron (bool): Allow voters to vote to "Re-open Nominations" when 
            voting for this position
        allow_abstain (bool): Allow votes to abstain from voting for a 
            candidate for this position
        positions_available (int): How many nominees can be successful in 
            applying for this position 
    """
    position = models.ForeignKey(
        to=f'{SocietyElectionsConfig.name}.{Position.__name__}',
        on_delete=models.CASCADE
    )
    election = models.ForeignKey(
        to=f'{SocietyElectionsConfig.name}.{Election.__name__}',
        on_delete=models.CASCADE,
        related_name='positions',
        related_query_name='position'
    )
    candidate_required = models.BooleanField(
        default=True,
        help_text='Whether or not at least one candidate is required in order '
        'to run this election'
    )
    allow_ron = models.BooleanField(
        default=True,
        help_text='Whether or not to include "Re-open Nominations" in the list '
        'of options for voters'
    )
    allow_abstain = models.BooleanField(
        default=True,
        help_text='Whether or not to allow voters to abstain from voting for '
        'this position'
    )
    positions_available = models.PositiveIntegerField(
        default=1,
        help_text='Number of available positions for this role'
    )

    def __str__(self):
        return f'{self.position.title} in {self.election.admin_title}'
