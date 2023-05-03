from django.shortcuts import render , redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login , logout ,authenticate
from .forms import applyingForm , appliedForm , interviewsForm
from .models import Applying , Applied , Interviews
import openai
from .key import api_key
import math
from django.contrib.auth.decorators import login_required




@login_required(login_url='/login/')
def home(request):
    context = {}
    applied = list(Applied.objects.filter(user = request.user).order_by('date').values())
    interviews = list(Interviews.objects.filter(user = request.user).order_by('date').values())



    applied_months = {'01':0,'02':0,'03':0,'04':0,'05':0,'06':0,'07':0,'08':0,'9':0,'10':0,'11':0,'12':0}
    interviews_months = {'01':0,'02':0,'03':0,'04':0,'05':0,'06':0,'07':0,'08':0,'9':0,'10':0,'11':0,'12':0}
    
    applied_scores = []
    applied_count = 0
    applied_sum = 0
    applied_success_rate = 0
    for i in applied:
        applied_scores.append(i['score'])
        applied_sum += i['score']
        if i['score'] >= 7:
            applied_success_rate += 1
        applied_count += 1
        applied_months[i['date'].strftime("%m")] += 1

    interviews_scores = []
    interviews_count = 0
    interviews_sum = 0
    interviews_success_rate = 0
    for i in interviews:
        interviews_scores.append(i['score'])
        interviews_sum += i['score']
        if i['score'] >= 7:
            interviews_success_rate += 1
        interviews_count += 1
        interviews_months[i['date'].strftime("%m")] += 1
    
    
    try:
        context['total_score_avg'] = "%.2f" % ((applied_sum + interviews_sum)/(applied_count + interviews_count))
    except:
        context['total_score_avg'] = 0
    try:
        context['total_success_rate'] = math.floor(((applied_success_rate + interviews_success_rate)/(applied_count + interviews_count))*100)
    except:
        context['total_success_rate'] = 0
    try:
        context['applied_score_avg'] ="%.2f" % (applied_sum/applied_count)
    except:
        context['applied_score_avg'] = 0
    try:
        context['interviews_score_avg'] ="%.2f" % (interviews_sum/interviews_count)
    except:
        context['interviews_score_avg'] = 0
    try:
        context['applied_success_rate'] = math.floor((applied_success_rate/applied_count)*100)
    except:
        context['applied_success_rate'] = 0
    try:
        context['interviews_success_rate'] = math.floor((interviews_success_rate/interviews_count)*100)
    except:
        context['interviews_success_rate'] = 0
        
        


    context['applied_scores'] = applied_scores
    context['interviews_scores'] = interviews_scores
    context['month_interviews'] = list(interviews_months.values())
    context['month_applied'] = list(applied_months.values())

    context['applied_count'] = applied_count
    context['interviews_count'] = interviews_count




    return render(request, 'tracker/home.html' , context)



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
        applied_table = Applied.objects.filter(user = request.user).order_by('-date')
    except:
        return redirect('/login')
    context ={'form':form ,'applied_table' :applied_table}
    return render(request, 'tracker/applied.html', context)

def interviews(request):
    if request.method == 'POST':
        form = interviewsForm(request.POST , request.FILES , user=request.user)
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
        form = interviewsForm(user=request.user)
    try:
        interviews_table = Interviews.objects.filter(user = request.user).order_by('-date')
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
    media_file = interview_to.recording

    response = openai.Audio.transcribe(
        api_key=API_KEY,
        model=model_id,
        file=media_file
    )
    interview_to.transcript = response['text']
    interview_to.save()
    return redirect(f'/interview/{id}')


def suggest(request , id):
    openai.api_key = api_key
    interview_to = Interviews.objects.get(id = id)
    text = interview_to.transcript

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "user", "content": f"PLay the role of a career coach. Based on the following tanscript from a recent interview i had, analyze my interviewee performance and suggest any ways i can improve (this is the format you should follow: ['OVERVIEW: ' + overall analysis + 'AREA TO IMPROVE: ' +  in no more than three words say an area where the user needs to improve based on the interview + 'SUGGESTION: ' + here include a suggestion based previous area to improve section(this section should be repeated at least twice, more if there are more than 2 areas to improve) + 'AREA OF STRENGTH: ' + in no more than three words say the area where the user most demonstrated proficiency + 'FEEDBACK: ' + here include your feedback on the user poficiency area])(refer to the interviewee as the user and the interviewer as the interviewer)(keep it brief and simple to understand)(use terms like 'should have')transcript: {text} ",}
        ]
    )
    interview_to.suggestions = response.choices[0].message.content
    interview_to.save()
    return redirect(f'/interview/{id}')