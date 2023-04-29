from django.shortcuts import render , redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login , logout ,authenticate
from .forms import applyingForm , appliedForm , interviewsForm
from .models import Applying , Applied , Interviews
import openai
from .key import api_key


def home(request):
    return render(request, 'tracker/home.html')

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

def interviews(request):
    if request.method == 'POST':
        form = interviewsForm(request.POST , request.FILES)
        if form.is_valid():
            company = form.cleaned_data['company']
            date = form.cleaned_data['date']
            result = form.cleaned_data['result']
            score = form.cleaned_data['score']
            application = form.cleaned_data['application']
            recording = request.FILES['recording']
            user = request.user
            new_interview = Interviews(user = user ,company = company , date = date , result = result ,  score = score , application = application , recording = recording)
            new_interview.save()
            return redirect('/interviews')
    else:
        form = interviewsForm()
    try:
        interviews_table = Interviews.objects.filter(user = request.user).order_by('-score')
    except:
        return redirect('/login')
    context ={'form':form ,'interviews_table' :interviews_table}
    return render(request, 'tracker/interviews.html', context)

def application(request , id):
    context = {}
    context['application'] = Applied.objects.get(id = id)
    return render(request, 'tracker/application.html' , context)


def interview(request , id):
    context = {}
    context['interview'] = Interviews.objects.get(id = id)
    return render(request, 'tracker/interview.html' , context)

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


def delete_applied(request , id):
    item = Applied.objects.get(id = id)
    item.delete()
    return redirect('/applied')

def delete_applying(request , id):
    item = Applying.objects.get(id = id)
    item.delete()
    return redirect('/applying')

def delete_interview(request , id):
    item = Interviews.objects.get(id = id)
    item.delete()
    return redirect('/interviews')

def transcribe(request , id):
    API_KEY = api_key
    model_id = 'whisper-1'
    interview_to = Interviews.objects.get(id = id)
    # media_file_path = interview_to.recording
    # media_file = open(media_file_path, 'rb')
    media_file = interview_to.recording

    response = openai.Audio.transcribe(
        api_key=API_KEY,
        model=model_id,
        file=media_file
    )
    interview_to.transcript = response['text']
    interview_to.save()
    return redirect(f'/interview/{id}')