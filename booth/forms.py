from django import forms

from booth.models import Creator


class PreviewAudioForm(forms.Form):
    creator_id = forms.CharField(max_length=6, required=True)
    language = forms.ChoiceField(choices=Creator.LANGUAGE_CHOICES, required=True)
    text = forms.CharField(max_length=64, required=True)
