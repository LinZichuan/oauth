from django.db import models

# Create your models here.

class User(models.Model):
	uid = models.CharField(max_length = 20)
	access_token = models.CharField(max_length = 40)
	name = models.CharField(max_length = 30)