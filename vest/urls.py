"""
URL configuration for vest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('core.urls')),
    path('accounts/', include('allauth.urls')),
    path('user/', include('user.urls')),
    path('deposit/',include('deposit.urls')),
    path('userprofile/', include('userprofile.urls')),
    path('withdraw/',include('withdraw.urls')),
    path('transfer/',include('transfer.urls')),
    path('kyc/',include('kyc.urls')),
    path('transaction/',include('transaction.urls')),
    path('bonus/',include('bonus.urls')),
    path('penalty/',include('penalty.urls')),
    path('contact/',include('contact.urls')),
    path('referral/',include('referral.urls')),
    path('plans/',include('investmentplan.urls')),
    path('faq/',include('faq.urls')),
    path('testimony/',include('testimony.urls')),
    path('statistic/',include('statistic.urls')),
    path('notification/',include('notification.urls')),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
  
handler404 = 'user.views.my_custom_page_not_found_view'
handler400 = 'user.views.my_custom_bad_request_view'
handler403 = 'user.views.my_custom_permission_denied_view'
handler500 = 'user.views.my_custom_error_view'
