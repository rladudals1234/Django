from django.db import models

# Create your models here.
class Member(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    pw = models.CharField(max_length=100, null=False)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    gender = models.CharField(max_length=2)
    age = models.IntegerField(default=0)
    hobby = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.id},{self.name},{self.age},{self.gender}"