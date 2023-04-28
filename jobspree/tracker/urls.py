from django.contrib import admin
from django.urls import path
from .views import home , sign_up

urlpatterns = [
    path('home', home , name='home'),
    path('sign-up', sign_up , name='sign-up')

]
