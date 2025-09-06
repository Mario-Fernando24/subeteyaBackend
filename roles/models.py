from django.db import models

# Create your models here.

from django.db import models

class Role(models.Model):
    id = models.CharField(max_length=50, primary_key=True, editable=True)
    name = models.CharField(max_length=100, unique=True)
    image = models.CharField(max_length=255)
    route = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'roles'
