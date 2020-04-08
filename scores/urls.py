from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    # url(r'^$',views.index,name='index'),
    # url(r'^details/(?P<id>\d+)/$',views.details,name='details')
    path('scores/',views.index,name='index'),
    path('',views.index,name='index'),
    path('democracy',views.democracy,name='democracy'),    


];
