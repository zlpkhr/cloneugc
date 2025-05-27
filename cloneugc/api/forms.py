from django import forms

from cloneugc.api.models import Actor


class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = ["name", "video"]
