from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    # url(r'^$',views.index,name='index'),
    # url(r'^details/(?P<id>\d+)/$',views.details,name='details')
    path('posts/',views.index,name='index'),
    path('',views.welcom,name='welcom'),
    path('about/',views.about,name='about'),
    path('welcom/',views.welcom,name='welcom'),
    path('posts/details/<int:id>/',views.details,name='details')


];
