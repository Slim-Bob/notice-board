from django.urls import path, include
from django.contrib.auth.views import LoginView

from .views import hello, send_email, logout_view, register, activate, account_activation_sent, create_ad, ad_my_list, \
    AdMyListView, AdCreateView, AdDetailView, AdUpdateView, AdsListView, add_response,  \
    confirmed_response, rejected_response

urlpatterns = [
    path('', hello, name='hello'),
    path('hello/', hello, name='hello'),
    path('email_send/', send_email, name='send_email'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', register, name='signup'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path('account_activation_sent/', account_activation_sent, name='account_activation_sent'),
    path('ad_create/', create_ad, name='ad_create'),
    # path('ad_my_list/', ad_my_list, name='ad_my_list'),
    path('ad_my_list/', AdMyListView.as_view(), name='ad_my_list'),
    path('ads/<slug:slug>/', AdDetailView.as_view(), name='ad_detail'),
    path('ads/<slug:slug>/edit', AdUpdateView.as_view(), name='ad_edit'),
    path('ads/', AdsListView.as_view(), name='ads'),
    path('ad/<int:ad_id>/add_response/', add_response, name='add_response'),
    path('response/<int:r_id>/confirmed', confirmed_response, name='confirmed_response'),
    path('response/<int:r_id>/rejected', rejected_response, name='rejected_response'),

    # path('ad_create/', AdCreateView.as_view(), name='ad_create'),
]