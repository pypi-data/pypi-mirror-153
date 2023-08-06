"""Some general purpose validators"""
from django.core.exceptions import ValidationError


def email_user_validator(email: str):
    """Ensures user portion of email consists of only alphanumeric characters, 
    dots, and dashes

    This is done to ensure that duplicate votes cannot be submitted for a given 
    email, by using various tricks like using a + character. Also ensures that 
    there is only one @ symbol in the whole email address.

    Args:
        email (str): Email to validate

    Raises:
        ValidationError: email does not have valid characters
    """
    valid_chars = (
        'abcdefghijklmnopqrstuvwxyz'
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        '1234567890-.'
    )
    email_parts = email.split('@')
    if len(email_parts) < 2:
        raise ValidationError(
            'Email does not have a domain, please enter a valid email address'
        )
    elif len(email_parts) > 2:
        raise ValidationError('Email is only permitted to have one @ character')
    
    # elif len(email_parts) == 0
    for char in email_parts[0]:
        if char not in valid_chars:
            raise ValidationError(
                'Email contains invalid character, only alphanumeric '
                'characters, dashes, and dots are allowed'
            )