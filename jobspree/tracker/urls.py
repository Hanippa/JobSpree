from django.contrib import admin
from django.urls import path
from .views import applied , applying , sign_up

urlpatterns = [
    path('applying', applying , name='applying'),
    path('applied', applied , name='applied'),
    path('sign-up', sign_up , name='sign-up')

]
