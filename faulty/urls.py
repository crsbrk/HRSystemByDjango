from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    # url(r'^$',views.index,name='index'),
    # url(r'^details/(?P<id>\d+)/$',views.details,name='details')
    path('', views.index, name='index'),
    path('faulty/', views.index, name='index'),
    path('details/<int:id>/', views.details, name='faulty'),

]
