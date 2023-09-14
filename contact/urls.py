from django.urls import path
from . import views

urlpatterns = [
        path('',views.user_contact, name='user_contact'),
        path('dashboard',views.dashboard_contact, name='dashboard_contact'),
        path('dashboard/<int:pk>',views.dashboard_contact_user, name='dashboard_contact_user'),
]