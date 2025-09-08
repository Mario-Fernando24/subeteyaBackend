from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

from users.models import User
class CustomJWTAuthentication(JWTAuthentication):

# Anular el método para extraer el usuario usando 'id' de la carga útil del token
    def get_user(self, validated_token):
        """
        Overrides the default method to use 'id' from the token payload instead of 'user_id'.
        """
        try:
            user_id = validated_token['id']
        except KeyError:
            raise AuthenticationFailed('El token no contenía ninguna identificación de usuario reconocible')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found', code='user_not_found')
        user.is_authenticated  = True
        return user     