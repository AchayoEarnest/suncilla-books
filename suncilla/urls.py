from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.services, name='services'),
    path('packages/', views.packages, name='packages'),
    path('industries/', views.industries, name='industries'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_post, name='blog_post'),
    path('contact/', views.contact, name='contact'),
    path('whatsapp/', views.whatsapp_redirect, name='whatsapp'),
]
