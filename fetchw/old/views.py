# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404

from .models import TestWeather, DummyUser, DummyQuery

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.generic import View
from .forms import UserLoginForm, RegisterForm

#landing page where user performs the search
def index(request):
    return render(request, 'fetchw/autocomplete.html')
    
    
    
def listing(request):
    # all_objects = TestWeather.objects.all()
    all_objects = DummyUser.objects.all()
    
    #use dictionary to pass db info to template
    context = {
        'all_objects': all_objects,
    }
    
    return render(request, 'fetchw/listing.html', context)

    
    
def detail(request, query_id):
    record = get_object_or_404(DummyUser, id=query_id)
    return render(request, 'fetchw/listing-detail.html', {'record': record})
    

def subloc(request):
    pass


def login_view(request):
    # form = UserLoginForm(request.POST or None)
    
    if request.method=='POST':
        # form = UserLoginForm(request.POST or None)
        form = UserLoginForm(data=request.POST)
        print form.is_valid()
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
    else:
        form = UserLoginForm()
        
    return render(request,'fetchw/login.html', {"form":form})
    
def register(request):
    form = RegisterForm(request.POST or None)
    return render(request,'register.html')

# class UserFormView(View):
#     form_class = UserForm
#     template_name = 'fetchw/register.html'
    
#     #blank user registration form
#     def get(self,request):
#         form = self.form_class(None)
#         return render(request, self.template_name, {'form':form})
    
#     #when user hits submit
#     def post(self,request):
#         form = self.form_class(data=request.POST)
#         print request.POST.keys()
#         print form
#         print form.is_bound
#         print form.is_valid()
        
#         if form.is_valid():
#             user = form.save(commit=False)
            
#             #clean data
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user.set_password(password)
#             user.save()
            
#             #get user object if pw and username are correct
#             user = authenticate(username=username, password=password)
            
#             if user is not None:
#                 #check if not restricted by admin
#                 if user.is_active:
#                     login(request, user) #now user is logged in
#                     return redirect('fetchw:index')
        
#         return render(request, self.template_name, {'form':form})            
                    
            
        
        
        
    
    