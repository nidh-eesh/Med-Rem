from django.urls import path
from . import views

urlpatterns = [
    path('index/',views.home, name='index'),
    path('appointment/',views.appointment, name='appointment'),
    path('records/',views.records, name ='record')
]
