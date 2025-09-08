from django.urls import path
from .views import update, updateWithImage, getUserById, getAllUsers

urlpatterns = {
    path('update/<id_user>', update, name='user-update'),
    path('apload/<id_user>', updateWithImage, name='user-apload'),
    path('getbyid/<id_user>', getUserById, name='user-getbyid'),
    path('getAllUsers', getAllUsers, name='user-getallusers'),

    
}