from django.contrib import admin
from student.models import Student
# from .models import Student   # .models앞에 생략도 가능

# Register your models here.
admin.site.register(Student)