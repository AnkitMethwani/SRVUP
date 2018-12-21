from django import forms
from django.db.models import Q
from videos.models import Video
from .models import Category
class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'order',
            'title',
            'video',
            'description',
            'slug',
        ]