from django.urls import path
from . import views
urlpatterns = [
    path("", views.user_bonus, name="user_bonus"),
     path("dashboard", views.dashboard_bonus, name="dashboard_bonus"),
     path("dashboard/<int:pk>", views.dashboard_bonus, name="dashboard_bonus")
]
