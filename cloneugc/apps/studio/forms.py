from django import forms

from .models import Ugc


class UgcForm(forms.ModelForm):
    class Meta:
        model = Ugc
        fields = ["creator", "script"]


class PreviewAudioForm(forms.Form):
    creator_id = forms.CharField(max_length=6, required=True)
    text = forms.CharField(required=True)
