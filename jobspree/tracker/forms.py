from django import forms
from django.contrib.auth.models import User
from .models import Applying , Applied

class applyingForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput() , required=False)
    class Meta:
        model = Applying
        fields = "__all__"
        exclude = ('user' ,)