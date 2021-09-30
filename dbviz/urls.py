from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('populate', views.populate, name='populate'),
    path('contact', views.contact, name='contact'),
]