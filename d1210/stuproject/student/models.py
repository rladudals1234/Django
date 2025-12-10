from django.db import models

# Create your models here.
# 테이블을 생성하면 항상 id - AutoField 생성됨.
# 테이블명 student_student형식으로 테이블이 생성됨.
class Student(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=1)
    grade = models.IntegerField(default=1)
    gender = models.CharField(max_length=10)
    hobby = models.CharField(max_length=100,default='게임')
    # kor = models.IntegerField(default=0)
    # eng = models.IntegerField(default=0)
    # math = models.IntegerField(default=0)
    # total = models.IntegerField(default=0)
    # avg = models.FloatField(default=0.0)
    # rank = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.sno},{self.name},{self.age},{self.grade},{self.gender},{self.hobby}"