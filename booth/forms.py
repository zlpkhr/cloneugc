from django import forms


class PreviewAudioForm(forms.Form):
    creator_id = forms.CharField(max_length=6, required=True)
    text = forms.CharField(max_length=64, required=True)


class ArucoBoardImgForm(forms.Form):
    screen_width = forms.IntegerField(required=True, min_value=1)
    screen_height = forms.IntegerField(required=True, min_value=1)
