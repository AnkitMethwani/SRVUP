from django import forms
from .models import Video


class VideoCreateForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'embed_code']
