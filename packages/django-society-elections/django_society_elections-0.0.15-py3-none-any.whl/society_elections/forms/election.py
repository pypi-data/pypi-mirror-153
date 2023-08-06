from django.forms import ModelForm

from ..models import Election

class ElectionForm(ModelForm):
    class Meta:
        model = Election
        exclude = (
            'email_winners',
            'email_losers',
            'winner_message',
            'loser_message'
        )