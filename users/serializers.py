from rest_framework import serializers
from .models import User
import bcrypt;

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','lastname','email','phone','image','password','notification_token']
        # es de escritura solamente
        extra_kwargs = {
            'password': {'write_only': True}
        }
    #donde se almacena la lógica de creación
    def create(self, validate_data):
        raw_password = validate_data.pop('password')
        hashed = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
        validate_data['password'] = hashed.decode('utf-8')  
        # accediendo a los objetos del modelo users
        # ** transforma el json en argumento
        user = User.objects.create(**validate_data)
        return user