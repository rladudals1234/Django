# coding: utf-8
from member.models import Member
Member.objects.all()
from student.models import Student
Student.objects.create(name='홍길동',kor=100,eng=100,math=100,total=300,avg=100.0,rank=1,grade='A')
Student.objects.all()
Student.objects.get(sno=1)
Student(name='홍길동',kor=100,eng=100,math=100,total=300,avg=100.0,rank=1,grade='A')
Student(name='홍길동',kor=100,eng=100,math=100,total=300,avg=100.0,rank=1,grade='A')
