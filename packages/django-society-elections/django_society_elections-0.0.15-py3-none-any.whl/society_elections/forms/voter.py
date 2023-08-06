from django import forms

from ..models import RegisteredVoter

class RegisteredVoterForm(forms.ModelForm):
    class Meta:
        model = RegisteredVoter
        exclude = ['election']