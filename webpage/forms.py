from django import forms
from .models import Beer
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field

class BeerForm(forms.ModelForm):

    class Meta:
        model = Beer
        fields = ('brewery', 'name', 'type', 'style', 'alcohol_content', 'blg')
