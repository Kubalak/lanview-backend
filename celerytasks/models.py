from django.db import models

# Create your models here.

class Task(models.Model):
    name = models.CharField(max_length=64)
    identifier = models.CharField(max_length=96)
    state = models.CharField(max_length=32)
