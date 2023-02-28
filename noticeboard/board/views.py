from django.shortcuts import render, redirect
from django.contrib.auth import logout

from .forms import EmailSendForm


def hello(request):
    return render(request, 'hello.html', {'user': request.user})


def send_email(request):
    if request.method == 'POST':
        form = EmailSendForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            header = form.cleaned_data['header']
            text = form.cleaned_data['text']

            print(email, header, text)
    else:
        form = EmailSendForm()
    return render(request, 'email_send.html', {'form': form})


def logout_view(request):
    next_page = request.GET.get('next', '/')
    print(next_page)
    logout(request)
    return redirect(next_page)