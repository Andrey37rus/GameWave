from django import forms
from django.core import validators
from django.contrib.auth.models import Group
from django.forms import ModelForm

from .models import Game


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)

        return result


class GameForm(forms.ModelForm):
    images = MultipleFileField(label='Image', required=False)

    class Meta:
        model = Game
        fields = ("name", "description", "age_rating", "genre", "system_requirements", "preview",)


