from django.db import models

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


    class Meta:
        db_table= 'users'


