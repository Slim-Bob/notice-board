from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    next = forms.CharField(widget=forms.HiddenInput(), required=False)


class EmailSendForm(forms.Form):
    email = forms.EmailField()
    header = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)

