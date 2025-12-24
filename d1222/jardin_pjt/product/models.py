from django.db import models

# Create your models here.
class Payment(models.Model):
    aid = models.CharField(max_length=50)
    tid = models.CharField(max_length=50)
    