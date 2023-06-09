from django.contrib import admin
from django.urls import path
from .views import applied , applying , sign_up , delete_applied, delete_applying , delete_interview , interviews , interview , transcribe , home , suggest , landing
from django.conf.urls.static import static
urlpatterns = [
    path('applying', applying , name='applying'),
    path('applied', applied , name='applied'),
    path('interviews', interviews , name='interviews'),
    path('sign-up', sign_up , name='sign-up'),
    path('delete-applying/<int:id>' , delete_applying),
    path('delete-applied/<int:id>' , delete_applied),
    path('delete-interview/<int:id>' , delete_interview),
    path('interview/<int:id>' , interview , name='interview'),
    path('transcribe/<int:id>' , transcribe , name='transcribe'),
    path('suggest/<int:id>' , suggest , name='suggest'),
    path('' , home , name='home'),
    path('home' , home , name='home'),
    path('landing' , landing , name='landing')

]
[]