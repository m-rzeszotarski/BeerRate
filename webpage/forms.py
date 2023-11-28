from django import forms
from .models import Beer
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field

class BeerForm(forms.ModelForm):

    class Meta:
        model = Beer
        fields = ('brewery', 'name', 'style', 'alcohol_content', 'blg')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Field('brewery', css_class="form50"),
            Field('name', css_class="form50"),
            Field('style', css_class="form50"),
            Field('alcohol_content', css_class="form10"),
            Field('blg', css_class="form10"),
        )
        self.helper.add_input(Submit('submit', 'Save'))
