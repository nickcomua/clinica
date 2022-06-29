from django.urls import path 
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('client/', ClientList.as_view()),
    path('client/<int:pk>/', ClientDetail.as_view()),
    path('worker/', WorkerList.as_view()),
    path('worker/<int:pk>/', WorkerDetail.as_view()),
    path('service/', ServiceList.as_view()),
    path('service/<int:pk>/', ServiceDetail.as_view()),
    path('location/', LocationList.as_view()),
    path('location/<int:pk>/', LocationDetail.as_view()),
    path('appointement/', AppointementList.as_view()),
    path('appointement/<int:pk>/', AppointementDetail.as_view()),
    path('user/', UserList.as_view()),
    path('user/<int:pk>/', UserDetail.as_view()),
    path('register/', register),
    #path('login/', login),
]


urlpatterns = format_suffix_patterns(urlpatterns)