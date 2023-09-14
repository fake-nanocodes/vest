from django.urls import path
from . import views

urlpatterns = [
       
         path('dashboard',views.dashboard_testimony, name='dashboard_testimony'),
          path('dashboard/delete/<int:pk>',views.dashboard_delete_testimony, name='dashboard_delete_testimony'),
]
