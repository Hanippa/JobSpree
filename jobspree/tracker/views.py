from django.shortcuts import render , redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login , logout ,authenticate
from .forms import applyingForm , appliedForm
from .models import Applying , Applied


def applying(request):
    if request.method == 'POST':
        form = applyingForm(request.POST)
        if form.is_valid():
            company = form.cleaned_data['company']
            keywords = form.cleaned_data['keywords']
            priority = form.cleaned_data['priority']
            user = request.user
            new_applying = Applying(company = company , keywords = keywords , priority = priority , user = user)
            new_applying.save()
            return redirect('/applying')
    else:
        form = applyingForm()
    try:
        applying_table = Applying.objects.filter(user = request.user).order_by('-priority')
    except:
        return redirect('/login')
    context ={'form':form ,'applying_table' :applying_table}
    return render(request, 'tracker/applying.html', context)

def applied(request):
    if request.method == 'POST':
        form = appliedForm(request.POST)
        if form.is_valid():
            company = form.cleaned_data['company']
            date = form.cleaned_data['date']
            result = form.cleaned_data['result']
            score = form.cleaned_data['score']
            user = request.user
            new_applied = Applied(user = user ,company = company , date = date , result = result ,  score = score)
            new_applied.save()
            return redirect('/applied')
    else:
        form = appliedForm()
    try:
        applied_table = Applied.objects.filter(user = request.user).order_by('-score')
    except:
        return redirect('/login')
    context ={'form':form ,'applied_table' :applied_table}
    return render(request, 'tracker/applied.html', context)




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