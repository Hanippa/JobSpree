from django import forms
from django.contrib.auth.models import User
from .models import Applying , Applied

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
    def __init__(self, *args, **kwargs):
        super(appliedForm, self).__init__(*args, **kwargs)
        self.fields['company'].label = ""
        self.fields['date'].label = ""
        self.fields['result'].label = ""
        self.fields['score'].label = ""