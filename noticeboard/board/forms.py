from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Ad, ResponseAd


class LoginForm(AuthenticationForm):
    next = forms.CharField(widget=forms.HiddenInput(), required=False)


class EmailSendForm(forms.Form):
    email = forms.EmailField()
    header = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)

    content = forms.CharField(widget=forms.Textarea)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class AdForm(forms.ModelForm):
    """Form for comments to the article."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["body"].required = False
        self.fields["category"].required = True

    class Meta:
        model = Ad
        fields = ['title', 'image', 'category', 'status', 'body']
        labels = {
            'title': 'Заголовок',
            'image': 'Картинка для привью',
            'category': 'Категория',
            'status': 'Статус',
            'body': 'Описание',
        }


class ResponseAdForm(forms.ModelForm):
    """Form for comments to the article."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["body"].required = False
        self.fields["author"].required = False
        self.fields["ad"].required = False
        self.fields["status"].required = False

    class Meta:
        model = ResponseAd

        fields = ['author', 'ad', 'body', 'status']
        labels = {
            'author': 'Автор',
            'ad': 'Объявление',
            'body': 'Текст',
            'status': 'Статус',
        }

