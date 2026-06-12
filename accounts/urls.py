from . import views
from django.urls import path

urlpatterns = [
    # url(r'^$',views.index,name='index'),
    # url(r'^details/(?P<id>\d+)/$',views.details,name='details')
    #path('',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout,name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('work-applications/',views.work_applications,name='work_applications'),
    path('approvals/',views.approvals,name='approvals'),
    path('work-application/<int:pk>/approve/',views.approve_work_application,name='approve_work_application'),
    path('work-application/<int:pk>/reject/',views.reject_work_application,name='reject_work_application'),
    path('work-application/<int:pk>/edit/',views.edit_work_application,name='edit_work_application'),
    path('work-application/<int:pk>/delete/',views.delete_work_application,name='delete_work_application'),
];
