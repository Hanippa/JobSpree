from django import forms
from django.contrib.auth.models import User
from .models import Applying , Applied , Interviews
from datetime import date

class applyingForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput() , required=False)
    class Meta:
        model = Applying
        fields = "__all__"
        exclude = ('user' ,)
    def __init__(self, *args, **kwargs):
        super(applyingForm, self).__init__(*args, **kwargs)
        self.fields['company'].label = ""
        self.fields['keywords'].label = ""
        self.fields['priority'].label = ""
class appliedForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput() , required=False)
    class Meta:
        model = Applied
        fields = "__all__"
        exclude = ('user' ,)
        widgets = {'date' : forms.DateInput(attrs={'type' : 'date'})}
    def __init__(self, *args, **kwargs):
        super(appliedForm, self).__init__(*args, **kwargs)
        self.fields['company'].label = ""
        self.fields['date'].label = ""
        self.fields['result'].label = ""
        self.fields['score'].label = ""

class interviewsForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput() , required=False)
    recording = forms.FileField(widget=forms.FileInput(attrs={'accept':'video/* , audio/*'}))
    class Meta:
        model = Interviews
        fields = ['company' , 'date' , 'result' , 'application' , 'score' ]
        widgets = {'date' : forms.DateInput(attrs={'type' : 'date'})}

    def __init__(self, *args, **kwargs):
        fuser = kwargs.pop('user')
        super(interviewsForm, self).__init__(*args, **kwargs)
        self.fields['application'].queryset = Applied.objects.filter(user = fuser)
        self.fields['company'].label = ""
        self.fields['date'].label = ""
        self.fields['result'].label = ""
        self.fields['score'].label = ""
        self.fields['application'].label = ""
        self.fields['recording'].label = ""
