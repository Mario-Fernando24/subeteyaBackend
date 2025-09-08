from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated      
from rest_framework.response import Response
from roles.models import Role
from roles.serializers import RoleSerializer
from subeteyabackend.settings import GLOBAL_HOST, GLOBAL_IP
from users.models import User
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile 
import os
import uuid
from django.utils.text import get_valid_filename
import logging

# CREAR USUARIO
@api_view(['PUT'])

@permission_classes([IsAuthenticated])
def update(request, id_user):
    if str(request.user.id) != str(id_user):
        return Response({
                'message': 'No tienes permiso para actualizar este usuario',
                'statusCode': status.HTTP_403_FORBIDDEN
                }, status=status.HTTP_403_FORBIDDEN)   

    try:
        user = User.objects.get(id=id_user)

    except User.DoesNotExist:
    
        return Response({
                'message': 'Email y la contraseña son obligatorios',
                'statusCode': status.HTTP_404_NOT_FOUND
                }, status=status.HTTP_404_NOT_FOUND)
    
    name = request.data.get('name', None)
    lastname = request.data.get('lastname', None)
    phone = request.data.get('phone', None)

    # Verificar si al menos un campo para actualizar fue proporcionado
    if name is None and lastname is None and phone is None:
        return Response({
                'message': 'No se enviaron datos para actualizar',
                'statusCode': status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST)
    
    # Actualizar los campos si se proporcionan nuevos valores
    if name is not None:
        user.name = name
    if lastname is not None:
        user.lastname = lastname
    if phone is not None:
        user.phone = phone    

    user.save()

    roles = Role.objects.filter(userhasrole__id_user=user)
    roles_serializer = RoleSerializer(roles, many=True)

    user_data = {
            "user": {   
            'id': user.id,
            'name': user.name,
            'lastname': user.lastname,
            'email': user.email,
            'phone': user.phone,
            'image': f'http://{GLOBAL_IP}:{GLOBAL_HOST}'+ user.image if user.image else None,
            'notification_token': user.notification_token,
            'roles': roles_serializer.data
            },
        }
    return Response(user_data, status=status.HTTP_200_OK)

 

# ACTUALIZAR IMAGEN DE USUARIO
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateWithImage(request, id_user):


    if str(request.user.id) != str(id_user):
        return Response({
                'message': 'No tienes permiso para actualizar este usuario',
                'statusCode': status.HTTP_403_FORBIDDEN
                }, status=status.HTTP_403_FORBIDDEN)   

    try:
        user = User.objects.get(id=id_user)

    except User.DoesNotExist:
    
        return Response({
                'message': 'Email y la contraseña son obligatorios',
                'statusCode': status.HTTP_404_NOT_FOUND
                }, status=status.HTTP_404_NOT_FOUND)
    
    # Obtener datos del request
    name = request.data.get('name', None)
    lastname = request.data.get('lastname', None)
    phone = request.data.get('phone', None)
    image = request.FILES.get('image', None)
   
    # Verificar si al menos un campo para actualizar fue proporcionado
    if name is None and lastname is None and phone is None and image is not None:
        return Response({
                'message': 'No se enviaron datos para actualizar',
                'statusCode': status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST)
    
    # Actualizar los campos si se proporcionan nuevos valores
    if name is not None:
        user.name = name
    if lastname is not None:
        user.lastname = lastname
    if phone is not None:
        user.phone = phone  
    if image:
     # Limpia nombre de archivo
     filename = get_valid_filename(image.name)

     # Genera nombre único para evitar colisiones
     ext = filename.split('.')[-1]
     filename = f"{uuid.uuid4()}.{ext}"

     # Path relativo a MEDIA_ROOT
     file_path = os.path.join("uploads", "users", str(user.id), filename)

     # Guardar archivo
     save_path = default_storage.save(file_path, ContentFile(image.read()))

    # Guardar URL en el modelo
    user.image = default_storage.url(save_path)
    user.save()

    roles = Role.objects.filter(userhasrole__id_user=user)
    roles_serializer = RoleSerializer(roles, many=True)

    user_data = {  
            'id': user.id,
            'name': user.name,
            'lastname': user.lastname,
            'email': user.email,
            'phone': user.phone,
            'image': f'http://{GLOBAL_IP}:{GLOBAL_HOST}'+ user.image if user.image else None,
            'notification_token': user.notification_token,
            'roles': roles_serializer.data
        }
    return Response(user_data, status=status.HTTP_200_OK)


#OBTENER USUARIO POR ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserById(request, id_user):
    try:
        user = User.objects.get(id=id_user)
    except User.DoesNotExist:
        return Response({
                'message': 'Usuario no encontrado',
                'statusCode': status.HTTP_404_NOT_FOUND
                }, status=status.HTTP_404_NOT_FOUND)

    roles = Role.objects.filter(userhasrole__id_user=user)
    roles_serializer = RoleSerializer(roles, many=True)

    user_data = {
        'id': user.id,
        'name': user.name,
        'lastname': user.lastname,
        'email': user.email,
        'phone': user.phone,
        'image': f'http://{GLOBAL_IP}:{GLOBAL_HOST}'+ user.image if user.image else None,
        'notification_token': user.notification_token,
        'roles': roles_serializer.data
        }
    return Response(user_data, status=status.HTTP_200_OK)




#OBTENER TODOS LOS USUARIOS
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAllUsers(request):
    # Obtener todos los usuarios
    users = User.objects.all()
    users_list = []

    for user in users:
        roles = Role.objects.filter(userhasrole__id_user=user)
        roles_serializer = RoleSerializer(roles, many=True)

        user_data = {
            'id': user.id,
            'name': user.name,
            'lastname': user.lastname,
            'email': user.email,
            'phone': user.phone,
            'image': f'http://{GLOBAL_IP}:{GLOBAL_HOST}'+ user.image if user.image else None,
            'notification_token': user.notification_token,
            'roles': roles_serializer.data
        }
        users_list.append(user_data)

    return Response(users_list, status=status.HTTP_200_OK)