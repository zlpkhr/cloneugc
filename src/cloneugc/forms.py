from django import forms

from cloneugc.models import Actor


class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = ["name", "video"]

class VideoForm(forms.Form):
    script = forms.CharField(required=True)