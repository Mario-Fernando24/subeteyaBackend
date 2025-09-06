from django.db import models

class UserHasRole(models.Model):
    id_user = models.ForeignKey('User', on_delete=models.CASCADE, db_column='id_user')
    id_role = models.ForeignKey('roles.Role', on_delete=models.CASCADE, db_column='id_role')

    class Meta:
        db_table = 'user_has_role'
        unique_together = ('id_user', 'id_role')


# Create your models here.
class User(models.Model):
    #id autoincremental
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    #el email no se puede repetir, es unico
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    image = models.CharField(max_length=255, null=True, blank=False)
    password = models.CharField(max_length=255)
    notification_token = models.CharField(max_length=255, null=True)
    create_at = models.DateTimeField(auto_now=True)
    update_at = models.DateTimeField(auto_now=True)
    #relacion muchos a muchos
    roles = models.ManyToManyField(
        'roles.Role',
         through='UserHasRole',
         related_name='users'
        )


    class Meta:
        db_table= 'users'


