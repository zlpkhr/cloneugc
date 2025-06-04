from django import forms

from .models import Ugc


class UgcForm(forms.ModelForm):
    class Meta:
        model = Ugc
        fields = ["creator", "script"]
