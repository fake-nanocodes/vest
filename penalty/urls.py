from django.urls import path
from . import views
urlpatterns = [
    path("", views.user_penalty, name="user_penalty"),
     path("dashboard", views.dashboard_penalty, name="dashboard_penalty"),
     path("dashboard/<int:pk>", views.dashboard_penalty, name="dashboard_penalty")
]