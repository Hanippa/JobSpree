from django.shortcuts import render , redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login , logout ,authenticate
from .forms import applyingForm
from .models import Applying , Applied


def home(request):
    if request.method == 'POST':
        form = applyingForm(request.POST)
        if form.is_valid():
            company = form.cleaned_data['company']
            keywords = form.cleaned_data['keywords']
            priority = form.cleaned_data['priority']
            user = request.user
            new_applying = Applying(company = company , keywords = keywords , priority = priority , user = user)
            new_applying.save()
            return redirect('/home')
    else:
        form = applyingForm()

    applying_table = Applying.objects.filter(user = request.user)
    context ={'form':form ,'applying_table' :applying_table}
    return render(request, 'tracker/home.html', context)





def sign_up(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request , user)
            return redirect('/home')
    else:
        form = UserCreationForm()

    return render(request , 'registration/sign-up.html' , {'form':form})