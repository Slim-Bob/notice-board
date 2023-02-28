from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import hello, send_email, logout_view

urlpatterns = [
    path('', hello, name='hello'),
    path('hello/', hello, name='hello'),
    path('email_send/', send_email, name='send_email'),
    path('login/', LoginView.as_view(), name='login'),
    #path('logout/', LogoutView.as_view(), name='logout'),
    path('logout/', logout_view, name='logout'),
]