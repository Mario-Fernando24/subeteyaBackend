from django.urls import path
from .views import register, login

urlpatterns = {
    path('register', register, name='user-register'),
    path('login', login, name='user-login'),

}