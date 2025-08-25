from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','lastname','email','phone','image','password','notification_token']


    def create(self, validate_data):
        # accediendo a los objetos del modelo users
        # ** transforma el json en argumento
        user = User.objects.create(**validate_data)
        return user