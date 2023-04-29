from django.contrib import admin
from django.urls import path
from .views import applied , applying , sign_up , delete_applied, delete_applying , delete_interview , interviews

urlpatterns = [
    path('applying', applying , name='applying'),
    path('applied', applied , name='applied'),
    path('interviews', interviews , name='interviews'),
    path('sign-up', sign_up , name='sign-up'),
    path('delete-applying/<int:id>' , delete_applying),
    path('delete-applied/<int:id>' , delete_applied),
    path('delete-interview/<int:id>' , delete_interview)

]
