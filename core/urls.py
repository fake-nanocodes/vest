from django.urls import path
from . import views


urlpatterns = [
                    path('about',views.about, name='about'),
                    path('banner',views.banner, name='banner'),
                    path('contact',views.contact, name='contact'),
                    path('faq',views.faq, name='faq'),
                    path('',views.index, name='index'),
                    path('payment',views.payment, name='payment'),
                    path('plans',views.plans, name='plans'),
                    path('terms',views.terms, name='terms'),

    ]
    #urls created
