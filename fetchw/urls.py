from django.conf.urls import url
from . import views

app_name = 'fetchw'

urlpatterns = [
       
    #/fetchw/
    url(r'^$', views.index, name='index'),
    
    #/fetchw/listing
    url(r'^listing/$', views.listing, name='listing'),
    
    #/fetchw/listing/2
    url(r'^listing/(?P<query_id>[0-9]+)$', views.detail, name='detail'),
    
    
    #/fetchw/login
    url(r'^login/$', views.login_view, name='login'),
    
    # #/fetchw/register
    # url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^register/$', views.register, name='register'),
    
    #/fetchw/search
    url(r'^search/$', views.search, name='search'),
    
    #/fetchw/timesearch
    url(r'^timesearch/$', views.timesearch, name='timesearch'),
    
]