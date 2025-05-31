from django import forms


class ArucoBoardImgForm(forms.Form):
    screen_width = forms.IntegerField(required=True, min_value=1)
    screen_height = forms.IntegerField(required=True, min_value=1)
