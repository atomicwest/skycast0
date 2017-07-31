# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect

from .models import TestWeather, DummyUser, DummyQuery

from django.contrib import auth
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.generic import View
from .forms import UserLoginForm, RegisterForm, SearchLocationForm, TimeSearchLocationForm

from django.http import HttpResponseRedirect, HttpResponse

from .getCurrentForecast import apiCurrentHandler
from .getTimeMachine import apiTimeMachineHandler


#landing page where user performs the search
def index(request):
    return render(request, 'fetchw/search.html')
    

def search(request):
    form = SearchLocationForm()
    if request.method=='POST':
        form = SearchLocationForm(request.POST)
        # print form
        # print form.is_valid()
        
        if form.is_valid():
            content = form.cleaned_data['location']
            print content
            #now pass content to api handlers
            weatherdata = apiCurrentHandler(content)
            # return HttpResponseRedirect("")
            return render(request, 'fetchw/results.html', {'form':form, 'weather':weatherdata})
    else:
        form = SearchLocationForm()
    return render(request, 'fetchw/search.html', {'form':form})


def timesearch(request):
    form = TimeSearchLocationForm()
    if request.method=='POST':
        form = TimeSearchLocationForm(request.POST)
        if form.is_valid():
            content = {}
            content['location'] = form.cleaned_data['location']
            content['startyear'] = form.cleaned_data['startyear']
            content['startmonth'] = form.cleaned_data['startmonth']
            content['startday'] = form.cleaned_data['startday']
            content['endyear'] = form.cleaned_data['endyear']
            content['endmonth'] = form.cleaned_data['endmonth']
            content['endday'] = form.cleaned_data['endday']
            
            #this dictionary should contain the plotly graph urls
            graphs = apiTimeMachineHandler(content)
            
            return render(request, 'fetchw/time-results.html', {'form': form, 'graphs': graphs })
    else:
        form = TimeSearchLocationForm()
    return render(request,'fetchw/time-search.html', {'form':form})




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


def login_view(request):
    form = UserLoginForm(request.POST or None)
    
    if request.method=='POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        print username
        print password
        print user
        if user is None:
            # return HttpResponseRedirect(reverse('error'))
            return render(request,'fetchw/login_fail.html', {"form":form})
        if not user.is_active:
            return render(request,'fetchw/login_fail.html', {"form":form})

        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        # return HttpResponseRedirect(reverse('home'))
        
    #     # form = UserLoginForm(request.POST or None)
    #     form = UserLoginForm(request.POST)
    #     testcred = {"username": "test", "password":"password123"}
    #     testform = UserLoginForm(testcred)
    #     print testform.is_valid()
    #     print form
    #     print form.is_valid()
    #     if form.is_valid():
    #         username = form.cleaned_data.get("username")
    #         password = form.cleaned_data.get("password")
    # else:
    #     form = UserLoginForm()
        
    return render(request,'fetchw/login.html', {"form":form})
    
def register(request):
    form = RegisterForm(request.POST or None)
    return render(request,'fetchw/register.html', {'form':form})

            
        
        
        
    
    