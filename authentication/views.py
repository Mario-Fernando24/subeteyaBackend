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
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny  

def getCustomTokenForUser(user):
    refresh_token = RefreshToken.for_user(user)
    del refresh_token.payload['user_id']
    refresh_token.payload['id'] = str(user.id)
    refresh_token.payload['name'] = str(user.name)
    return refresh_token   # 👈 no lo conviertas a string aquí

# CREAR USUARIO
@api_view(['POST'])
@permission_classes([AllowAny])
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

        refresh = getCustomTokenForUser(user)

        access_token = str(refresh.access_token)     


        response_data = {
            "user": {
                **serializer.data,
                'roles': roles_serializer.data
            },
            'access_token': 'Bearer '+ access_token
        }
    
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    error_message = []
    for field, errors in serializer.errors.items():
            for error in errors:
                error_message.append(f"{field}: {error}")   

    error_response = {
            "message": error_message,
            "statusCode": status.HTTP_400_BAD_REQUEST
   }        

    return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
 

#LOGIN
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({
            'message': 'Email y la contraseña son obligatorios',
            'statusCode': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        #obtener usuario por email
        user = User.objects.get(email=email)

    except User.DoesNotExist:
        return Response({
            'message': 'Las credenciales no son validas',
            'statusCode': status.HTTP_401_UNAUTHORIZED
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
         
        refresh = getCustomTokenForUser(user)

        access_token = str(refresh.access_token)     

         # Obtener y asignar los roles del usuario
        roles = Role.objects.filter(userhasrole__id_user=user)
        # marshall the roles
        roles_serializer = RoleSerializer(roles, many=True)

        user_data = {
            "user": {   
            'id': user.id,
            'name': user.name,
            'lastname': user.lastname,
            'email': user.email,
            'phone': user.phone,
            'image': user.image,
            'notification_token': user.notification_token,
            'roles': roles_serializer.data
            },
            'access_token': 'Bearer '+ access_token   

        }
        #serializer = UserSerializer(user_data)
        return Response(user_data, status=status.HTTP_200_OK)
    else:    
        return Response({'message': 'Las credenciales no son validas','statusCode':status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)
                        

