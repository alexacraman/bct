from django.urls import path
from . import views

app_name='donate'

urlpatterns = [
    path('receive/', views.receive_donation, name='receive'),
    path('success/', views.donation_success, name='success'),
    path('webhook/', views.webhook, name="webhook"),

    path('donations/', views.DonationsListView.as_view(), name="donations"),
    path('donations-data/', views.donation_json, name='donations-data'),
]



