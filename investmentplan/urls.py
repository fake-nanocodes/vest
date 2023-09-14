from django.urls import path
from . import views

urlpatterns = [
        path('',views.user_plan, name='user_plan'),
        path('history',views.user_plan_history, name='user_plan_history'),
         path('dashboard',views.dashboard_investment_plan, name='dashboard_investment_plan'),
          path('dashboard/delete/<int:pk>',views.dashboard_delete_investment_plan, name='dashboard_delete_investment_plan'),
]
