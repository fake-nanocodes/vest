from django.urls import path
from . import views

urlpatterns = [
       
         path('dashboard',views.dashboard_faq, name='dashboard_faq'),
          path('dashboard/delete/<int:pk>',views.dashboard_delete_faq, name='dashboard_delete_faq'),
]
