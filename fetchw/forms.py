from django.contrib.auth.models  import User
from django import forms
from django.contrib.auth import authenticate, login, logout, get_user_model

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

import datetime

# User = get_user_model()

# class UserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
    
#     #info about class
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']

class SearchLocationForm(forms.Form):
    location = forms.CharField(required=True)
    # print location
    def clean(self):
      data = self.cleaned_data['location']
    #   data = self.cleaned_data
    
    #   #raise ValidationError()
       
    #   return data
    # class Meta:
    #     fields = ['location']
    

class TimeSearchLocationForm(forms.Form):
    location = forms.CharField(required=True)
    thisyear = datetime.datetime.now().year
    startyear = forms.ChoiceField(choices=[(x,x) for x in range(1970, thisyear+1)])
    endmonth = forms.ChoiceField(choices=[(x,x) for x in range(1970, thisyear+1)])
    endyear = forms.ChoiceField(choices=[(x,x) for x in range(1970, thisyear+1)])

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    #check if user active or registered
    
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username,password=password)
        if not user:
            raise forms.ValidationError("User does not exist")
        
        if not user.check_password(password):
            raise forms.ValidationError("Password not correct")
        
        if not user.is_active:
            raise forms.ValidationError("User not logged in")
        
        # return super(UserLoginForm, self).clean(*args, **kwargs)
        return {"username": username, "password": password}
        
        
class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)