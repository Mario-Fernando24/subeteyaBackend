from django.urls import path
from .views import update, updateWithImage

urlpatterns = {
    path('update/<id_user>', update, name='user-update'),
    path('apload/<id_user>', updateWithImage, name='user-apload'),
    
}