from django.urls import path
from . import views

urlpatterns = [
        path('',views.user_dashboard, name='user_dashboard'),
        path('dashboard',views.admin_dashboard, name='admin_dashboard'),
         path('dashboard/users',views.admin_dashboard_user, name='admin_dashboard_user'),
          path('dashboard/user/<int:pk>',views.admin_dashboard_user_detail, name='admin_dashboard_user_detail'),
           path('dashboard/admin_add_user_deposit/<int:pk>',views.admin_add_user_deposit, name='admin_add_user_deposit'),
        path('dashboard/admin_add_user_withdrawal/<int:pk>',views.admin_add_user_withdrawal, name='admin_add_user_withdrawal'),
        path('dashboard/user_password_reset_by_admin/<int:pk>',views.user_password_reset_by_admin, name='user_password_reset_by_admin'),
        path('dashboard/admin_make_investment_for_user/<int:pk>',views.admin_make_investment_for_user, name='admin_make_investment_for_user'),
        path('dashboard/editbalance/<int:pk>',views.editbalance, name='editbalance'),
        path('dashboard/user_profile_update_by_admin/<int:pk>',views.user_profile_update_by_admin, name='user_profile_update_by_admin'),
        path('dashboard/delete/<int:pk>',views.delete_user, name='delete_user'),
]