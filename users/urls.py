from django.urls import path
from .views import create, list_users

urlpatterns = {
    path('', create, name='user-create'),
    path('/list', list_users, name='user-list'),
}