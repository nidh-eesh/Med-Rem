from django.urls import path
from . import views

urlpatterns = [
    path('index/',views.home, name='index'),
    path('records/',views.records, name ='record')
]
