from django.urls import path
from . import views

urlpatterns = [
       
         path('dashboard',views.dashboard_statistic, name='dashboard_statistic'),
          path('dashboard/delete/<int:pk>',views.dashboard_delete_statistic, name='dashboard_delete_statistic'),
]
