from django import forms

from .models import Course, Lecture


class LectureAdminForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = [
            'order',
            'title',
            'free',
            'video',
            'description',
            'slug',
        ]

class CourseForm(forms.ModelForm):
    # number = forms.IntegerField()
    class Meta:
        model = Course
        fields = [
            'title',
            'description',
            'slug',
            'price',

        ]