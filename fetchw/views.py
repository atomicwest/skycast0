# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect

from .models import Query

from django.contrib import auth
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
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
            # print content
            
            #if a user is logged in, copy the location to a query object
            #associate with the user id, then save query object to db
            if request.user.is_authenticated():
                print request.user.id
                q = Query(userid=request.user, query=content)
                q.save()
                
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
            
            
            #if a user is logged in, copy the location to a query object
            #associate with the user id, then save query object to db
            if request.user.is_authenticated():
                recorddate = "%s | Start on %s-%s-%s, End on %s-%s-%s" % (content['location'],
                    content['startyear'],content['startmonth'], content['startday'], 
                    content['endyear'], content['endmonth'], content['endday']
                )
                q = Query(userid=request.user, query=recorddate)
                q.save()
            
            #this dictionary should contain the plotly graph urls
            graphs = apiTimeMachineHandler(content)
            
            return render(request, 'fetchw/time-results.html', {'form': form, 'graphs': graphs })
    else:
        form = TimeSearchLocationForm()
    return render(request,'fetchw/time-search.html', {'form':form})


def register(request):
    form = RegisterForm()
    if request.method=='POST':
        form = RegisterForm(request.POST)
        
        print form
        print form.is_valid()
        
        if form.is_valid():
            userinfo = {}
            userinfo['username'] = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            # userinfo['password'] = form.cleaned_data['password']
            userinfo['email'] = form.cleaned_data['email']
            
            #check database to see if user exists
            
            user = User.objects.create_user(userinfo['username'], userinfo['email'],pw)
            
            #authenticate and bring to user profile page
            # user = authenticate(request, username=userinfo['username'], password=pw)
            # user = authenticate(username=userinfo['username'], password=pw)
            
            if user is not None:
                login(request, user)
                return render(request,'fetchw/user-profile.html', {'form':form, 'userinfo':userinfo})
            else:
                return render(request,'fetchw/register.html', {'form':form})
            
    return render(request,'fetchw/register.html', {'form':form})
    

def logout_view(request):
    logout(request)
    return render(request, 'fetchw/search.html', {})

def login_view(request):
    form = UserLoginForm(request.POST or None)
    
    if request.method=='POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        print username
        
        print user
        if user is not None:
            # return HttpResponseRedirect(reverse('error'))
            login(request,user)
            return render(request,'fetchw/user-profile.html', {"form":form})
        else:
            return render(request,'fetchw/login_fail.html', {"form":form})


        
    return render(request,'fetchw/login.html', {"form":form})
    


def homepage(request):
    
    if request.user.is_authenticated():
        queries = Query.objects.filter(userid=request.user.id)
        return render(request,'fetchw/user-profile.html', {'queries':queries})
    else:
        return render(request,'fetchw/search.html')
        
    
    