from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from users.serializers import UserSerializer
import logging

# Create your views here.

@api_view(['POST'])
def create(request):
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
 


# 🔹 Nuevo endpoint para listar usuarios
@api_view(['GET'])
def list_users(request):
    logging.critical("RESPONDIO  ")
    return Response(status=status.HTTP_200_OK)