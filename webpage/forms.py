from django import forms
from .models import Beer, Review
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth. models import User


# Form for creation of the new beer in the database
class BeerForm(forms.ModelForm):

    class Meta:
        model = Beer
        fields = ('brewery', 'name', 'style', 'alcohol_content', 'blg', 'picture')

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
            Field('picture', css_class="form50"),
        )
        self.helper.add_input(Submit('submit', 'Save'))


# Form for creation of the new review (rating and comment about beer existing in the database)
class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('score', 'comment')

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
            Field('score', css_class="form10"),
            Field('comment', css_class="form50"),
        )
        self.helper.add_input(Submit('submit', 'Save'))


# Form for creating new accounts
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
