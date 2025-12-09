from django.db import models

# Create your models here.
class Student(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    kor = models.IntegerField()
    eng = models.IntegerField()
    math = models.IntegerField()
    total = models.IntegerField()
    avg = models.FloatField()
    rank = models.IntegerField()
    grade = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.sno},{self.name},{self.kor},{self.eng},{self.math},{self.total},{self.avg},{self.rank},{self.grade}"
    