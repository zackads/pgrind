from django import forms
from pgrind.models.attempt import Attempt


class AttemptForm(forms.ModelForm):
    class Meta:
        model = Attempt
        fields = ["confidence"]
