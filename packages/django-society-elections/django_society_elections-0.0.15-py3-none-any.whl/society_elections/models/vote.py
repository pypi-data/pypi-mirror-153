from django.db import models

from ..apps import SocietyElectionsConfig
from .candidate import Candidate
from .electionposition import ElectionPosition
from .voter import AnonymousVoter, RegisteredVoter


class Vote(models.Model):
    f"""Represents a vote from a voter for a particular election candidate (or 
    RON/Abstain

    Attributes:
        registered_voter ({RegisteredVoter.__name__}): Registered voter in the 
            election if election is not anonymous
        anonymous_voter ({AnonymousVoter.__name__}): Anonymous voter in the     
            election if the election is anonymous
        candidate ({Candidate.__name__}): Candidate in the election
        position ({ElectionPosition.__name__}): The position being voted for
        ron (bool): Whether or not the voter voted to re-open nominations
        abstain (bool): Whether or not the voter voter to abstain
        vote_cast_at (datetime): Time the vote was cast
        vote_last_modified_at (datetime): Time the vote was last modified, 
            useful to understand if someone has changed their vote
    """
    registered_voter = models.ForeignKey(
        to=f'{SocietyElectionsConfig.name}.{RegisteredVoter.__name__}',
        on_delete=models.CASCADE,
        editable=False,
        null=True
    )
    anonymous_voter = models.ForeignKey(
        to=f'{SocietyElectionsConfig.name}.{AnonymousVoter.__name__}',
        on_delete=models.CASCADE,
        editable=False,
        null=True
    )
    candidate = models.ForeignKey(
        to=f'{SocietyElectionsConfig.name}.{Candidate.__name__}',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='votes',
        related_query_name='vote'
    )
    position = models.ForeignKey(
        to=f'{SocietyElectionsConfig.name}.{ElectionPosition.__name__}',
        on_delete=models.CASCADE,
        related_name='votes',
        related_query_name='vote',
        editable=False
    )
    vote_cast_at = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    vote_last_modified_at = models.DateTimeField(
        auto_now=True,
        editable=False
    )

    @property
    def is_anonymous(self) -> bool:
        """bool:  True if election is anonymous, False otherwise"""
        return self.position.election.anonymous

    @property
    def voter_str(self) -> str:
        """str: String representation of the voter"""
        if self.anonymous_voter is None:
            return str(self.registered_voter)
        else:
            return f'Anonymous Voter {self.anonymous_voter}'

    @property
    def voter_pk(self) -> str:
        """str: String representing the primary key of the voter"""
        if self.anonymous_voter is None:
            return str(self.registered_voter.pk)
        else:
            return str(self.anonymous_voter.pk)

    def __str__(self):
        return f'{self.voter_str} voting {self.candidate}'
