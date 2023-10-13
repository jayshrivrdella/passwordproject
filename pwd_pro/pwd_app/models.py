from django.db import models


# Create your models here.
class Users(models.Model):
    username = models.CharField(unique=True, max_length=100)
    hashvalue = models.CharField(max_length=100)
    salt = models.CharField(max_length=100)
    userid = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'users'
