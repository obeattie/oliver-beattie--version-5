"""Forms for the links application."""
from django import forms

from obeattie.links.models import Link

class QuickAddForm(forms.ModelForm):
    """Form for quickly adding a link to the site."""
    class Meta:
        model = Link
        exclude = ('created', 'last_modified', )
