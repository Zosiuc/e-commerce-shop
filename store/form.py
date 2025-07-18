# forms.py

from django import forms
from .models import Group


class AddToFavoritesForm(forms.Form):
    group = forms.ModelChoiceField(queryset=Group.objects.none(), required=False)
    new_group = forms.CharField(required=False, max_length=100)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = Group.objects.filter(user=user)
