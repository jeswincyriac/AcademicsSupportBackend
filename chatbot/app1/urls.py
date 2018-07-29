from django.urls import path,include
from .views import message,login

urlpatterns = [
    path('login',login, name='login'),
    path('message',message, name='message'),

]
