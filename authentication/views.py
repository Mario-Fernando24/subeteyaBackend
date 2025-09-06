import bcrypt
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from users.models import User
from users.serializers import UserSerializer
import logging
from rest_framework_simplejwt.tokens import RefreshToken    
# CREAR USUARIO
@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data = request.data)

    if request.method == 'POST':
        logging.debug("Este es un log de depuración")
        logging.info("Este es un log de información")
        logging.warning("Este es un log de advertencia")
        logging.error("Este es un log de error")
        logging.critical("Este es un log crítico")

    if serializer.is_valid():
        serializer.save()
    
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 


#LOGIN
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Email y la contraseña son obligatorios'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        #obtener usuario por email
        user = User.objects.get(email=email)

    except User.DoesNotExist:
        return Response({'error': 'Las credenciales no son validas'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
         
        refresh = RefreshToken.for_user(user)

        access_token = str(refresh.access_token)     

        user_data = {
            "user": {   
            'id': user.id,
            'name': user.name,
            'lastname': user.lastname,
            'email': user.email,
            'phone': user.phone,
            'image': user.image,
            'notification_token': user.notification_token,
            },
            'access_token': 'Bearer '+ access_token   

        }
        #serializer = UserSerializer(user_data)
        return Response(user_data, status=status.HTTP_200_OK)
    else:    
        return Response({'error': 'Las credenciales no son validas'}, status=status.HTTP_401_UNAUTHORIZED)
                        

