import bcrypt
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from roles.models import Role
from roles.serializers import RoleSerializer
from users.models import User, UserHasRole
from users.serializers import UserSerializer
import logging
from rest_framework_simplejwt.tokens import RefreshToken  

# CREAR USUARIO
@api_view(['POST'])
def register(request):

    serializer = UserSerializer(data = request.data)

    if serializer.is_valid():

        user=serializer.save()

        client_role =get_object_or_404(Role, id='CLIENTE')
        # Asignar el rol de cliente al usuario
        UserHasRole.objects.create(id_user = user, id_role=client_role)
        # Obtener y asignar los roles del usuario
        roles = Role.objects.filter(userhasrole__id_user=user)
        # marshall the roles
        roles_serializer = RoleSerializer(roles, many=True)

        response_data = {
            **serializer.data,
            'roles': roles_serializer.data
        }
    
        return Response(response_data, status=status.HTTP_201_CREATED)
    
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
                        

