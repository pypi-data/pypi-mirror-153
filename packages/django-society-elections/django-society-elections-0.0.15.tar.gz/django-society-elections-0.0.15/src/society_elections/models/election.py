from django.conf import settings
from django.db import models
from django.utils import timezone


class Election(models.Model):
    f"""A first-past-the-post election
    
    An election is an event in two parts: nominations and voting. Nominations 
    run from a given time UTC to a given time UTC. During this time candidates 
    can nominate themselves for a given election position. Voting takes place 
    from a given time UTC (which must be after the end of nominations), to a 
    given time UTC. During this time, voters vote for candidates for positions.

    Voters will have a minimum and maximum number of votes that they can cast 
    for any given position, with the maximum number of votes generally 
    indicating how many positions are available for that given position.

    Attributes:
        title (str): Title of the election, displayed as the title of the pages
        admin_title (str): Title displayed only in the admin page, which 
            provides differentiation between annual elections
        description (str): Why the election is taking place
        created_by ({settings.AUTH_USER_MODEL}): Who created the election
        created_at (datetime): When the election was created
        nominations_start (datetime): When the nominations start
        nominations_end (datetime): When the nominations end
        voting_start (datetime): When the voting period starts
        voting_end (datetime): When the voting period ends,
        voter_email_domain_whitelist (str): An optional, newline delimited 
            whitelist of which email domains to allow voting from
        candidate_email_domain_whitelist (str): An optional, newline delimited 
            whitelist of which email domains to allow nominations from
        email_winners (bool): Whether or not to email the winners of an election
        email_losers (bool): Whether or not to email the losers of an election
        winner_message (str): The message to send successful candidates
        loser_message (str): The message to send unsuccessful candidates
        results_submitted (bool): Whether or not the results have been finalised
        results_submitted_by ({settings.AUTH_USER_MODEL}): Who finalised the 
            results
        results_submitted_at (datetime): When were the results finalised
        positions (object): one-to-many relation to ElectionPosition
        anonymous (bool): Whether or not the votes should be anonymized
        NOMINATIONS (str): Represents the nomination period of the election
        VOTING (str): Representing the voting period of the election
        INTERIM (str): Represents the time between nominations and voting
        PRENOMINATION (str): Represents the time before nominations begin
        POSTVOTING (str): Represents the time after voting has finished
        FINISHED (str): Represents that the election has finished
    """
    title = models.CharField(
        max_length=100
    )
    admin_title = models.CharField(
        max_length=500,
        help_text='Title displayed only in the admin pages, which provides '
        'differentiation between e.g. annual elections'
    )
    description = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.PROTECT,
        editable=False,
        related_name='elections_created',
        related_query_name='election_created'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    nominations_start = models.DateTimeField(
        verbose_name='nominations start time'
    )
    nominations_end = models.DateTimeField(
        verbose_name='nominations end time'
    )
    voting_start = models.DateTimeField(
        verbose_name='voting period start time'
    )
    voting_end = models.DateTimeField(
        verbose_name='voting period end time'
    )
    voter_email_domain_whitelist = models.TextField(
        help_text='Newline-delimited list of email domains to accept when '
        'voters sign up to vote in the election',
        blank=True,
        null=True
    )
    candidate_email_domain_whitelist = models.TextField(
        help_text='Newline-delimited list of email domains to accept when '
        'candidates nominate themselves in the election'
    )
    email_winners = models.BooleanField(
        default=False
    )
    email_losers = models.BooleanField(
        default=False
    )
    verify_candidate_emails = models.BooleanField(
        default=False
    )
    winner_message = models.TextField(
        help_text='The message to send to successful candidates in an election.'
        ' Format the message by using {name} for the candidate name, {position}'
        ' for the title of the position, and {votes} for the number of votes '
        'they received',
        blank=True,
        null=True
    )
    loser_message = models.TextField(
        help_text='The message to send to unsuccessful candidates in an '
        'election. Format the message by using {name} for the candidate name, '
        '{position} for the title of the position, and {votes} for the number '
        'of votes they received',
        blank=True,
        null=True
    )
    candidate_verification_email = models.TextField(
        help_text='The message to send to candidates to verify their email in '
        'an election. Format the message by using {name} for the candidate '
        'name, {position} for the title of the position, and {verify_url} for '
        'the link to verify their email',
        blank=True,
        null=True
    )
    voter_verification_email = models.TextField(
        help_text='The message to send to voters to verify their email in the election. Format the message by using {email} for the voter\'s email address, and {verify_url} for the link to verify their email',
        default='Click the link below or copy into your browser to verify your '
        'email address:\n\n{verify_url}'
    )
    ended_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=False,
        editable=False,
        related_name='elections_ended',
        related_query_name='election_ended'
    )
    ended_at = models.DateTimeField(
        blank=False,
        null=True,
        editable=False
    )
    anonymous = models.BooleanField(
        default=True,
    )

    NOMINATIONS = 'nominations'
    VOTING = 'voting'
    INTERIM = 'interim'
    PRENOMINATION = 'pre-nomination'
    POSTVOTING = 'post-voting'
    FINISHED = 'finished'
    ELECTION_PERIODS = (
        NOMINATIONS, VOTING, INTERIM, PRENOMINATION, POSTVOTING, FINISHED
    )

    def __str__(self):
        return self.admin_title

    @property
    def current_period(self) -> str:
        """str: Returns the period the election is currently in"""
        now = timezone.now()
        if self.ended_by is not None:
            return self.FINISHED
        elif self.nominations_start <= now and self.nominations_end > now:
            return self.NOMINATIONS
        elif self.voting_start <= now and self.voting_end > now:
            return self.VOTING
        elif self.nominations_end <= now and self.voting_start > now:
            return self.INTERIM
        elif self.nominations_start > now:
            return self.PRENOMINATION
        else:
            return self.POSTVOTING
        

    class Meta:
        app_label = 'society_elections'
        ordering = ['-nominations_start', 'admin_title']
        get_latest_by = ['nominations_start']
