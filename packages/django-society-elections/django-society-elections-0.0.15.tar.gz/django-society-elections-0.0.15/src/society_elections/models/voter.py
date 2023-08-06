import secrets
import uuid
from hashlib import sha512

from django.core.mail import send_mail
from django.db import models
from django.urls import reverse

from .. import app_settings
from ..apps import SocietyElectionsConfig
from ..validators import email_user_validator
from .election import Election


class RegisteredVoter(models.Model):
    f"""Represents a registered in the database

    This model represents a voter who has registered in the database. The email 
    is stored in plaintext, but anonymous elections will not link this model to 
    any votes.
    
    Attributes:
        id (UUID): Unique identifier for a voter in the database. A UUID is 
            used to prevent guessable voter IDs
        election ({Election.__name__}): The election the voter is signed up to
            vote in
        email (str): Email of the registered voter - required to resend 
            verification emails
        verified (bool): Has the voter verified their email address
        registered_at (datetime): The time the voter registered
        verified_at (datetime): When the voter verified their email
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    election = models.ForeignKey(
        to=f'{SocietyElectionsConfig.name}.{Election.__name__}',
        on_delete=models.CASCADE,
        related_name='registered_voters',
        related_query_name='registered_voter'
    )
    email = models.EmailField(
        validators=[email_user_validator]
    )
    registered_at = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    verified_at = models.DateTimeField(
        blank=True,
        null=True,
        editable=False
    )

    @property
    def verified(self) -> bool:
        return self.verified_at is not None

    @property
    def verify_url(self) -> str:
        """str: URL to click to verify the email address of a voter"""
        return (
            app_settings.ROOT_URL + reverse(
                'society_elections:voter_verify'
            ) + f'?uuid={self.pk}'
        )

    def send_verification_email(self) -> None:
        """Sends a verification email to the voter

        Raises:
            ValueError: Voter has not yet been saved to the database
        """
        if self.verified:
            return
        elif self.pk is None:
            raise ValueError(
                'Voter has not yet been saved to the database, cannot send '
                'email until we have a primary key to validate against.'
            )
        else:
            message = self.election.voter_verification_email.format(
                email=self.email,
                verify_url=self.verify_url
            )
            send_mail(
                f'Verify Email for Voting in {self.election}',
                message, None, [self.email,], html_message=message
            )

    def __str__(self):
        return str(self.id)


class AnonymousVoter(models.Model):
    f"""Represents an Anonymized voter in the database

    Emails are not linked to this model. Instead, voters use a unique (non-cryptographically secure) "password" which is stored hashed in the database without a salt. They use this password to vote anonymously.

    Attributes:
        election ({Election.__name__}): Election this voter is voting in
        password (bytes): SHA512 digest of the voter password in the database - 
            this is randomly generated for each user once their email is 
            verified
    """
    election = models.ForeignKey(
        to=f'{SocietyElectionsConfig.name}.{Election.__name__}',
        on_delete=models.CASCADE,
        related_name='anonymous_voters',
        related_query_name='anonymous_voter'
    )
    password = models.BinaryField(
        editable=False,
        unique=True
    )

    @staticmethod
    def generate_voter_password() -> str:
        """Generates a new random password for the anonymous voter

        Returns:
            str: Randomly generated password
        """
        characters = (
            'abcdefghijklmnopqrstuvwxyz'
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            '1234567890-_'
        )
        return ''.join([secrets.choice(characters) for _ in range(16)])

    @staticmethod
    def hash_password(password: str) -> bytes:
        """Hash the given password and return the raw digest

        Args:
            password (str): Password to hash

        Returns:
            bytes: SHA512 hash digest of the password
        """
        hash = sha512()
        hash.update(password.encode())
        return hash.digest()

    def __str__(self):
        return str(self.pk)