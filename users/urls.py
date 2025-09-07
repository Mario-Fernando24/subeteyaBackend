from django.urls import path
from .views import update

urlpatterns = {
    path('update/<id_user>', update, name='user-update'),
}