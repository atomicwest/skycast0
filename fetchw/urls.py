from django.conf.urls import url
from . import views

app_name = 'fetchw'

urlpatterns = [
       
    #/fetchw/
    url(r'^$', views.index, name='index'),
    
    #/fetchw/login
    url(r'^login/$', views.login_view, name='login'),
    
    #/fetchw/logout
    url(r'^logout/$', views.logout_view, name='logout'),
    
    # #/fetchw/register
    # url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^register/$', views.register, name='register'),
    
    #/fetchw/search
    url(r'^search/$', views.search, name='search'),
    
    #/fetchw/timesearch
    url(r'^timesearch/$', views.timesearch, name='timesearch'),
    
    #/fetchw/homepage
    url(r'^homepage/$', views.homepage, name='homepage'),
    
]