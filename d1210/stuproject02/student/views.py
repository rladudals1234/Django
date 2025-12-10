from django.shortcuts import render, redirect
from student.models import Student
from django.urls import reverse

# Create your views here.
def write(request):
    if request.method == 'GET':
        return render(request,'student/write.html')
    elif request.method == 'POST':
        name = request.POST.get("name")
        age = request.POST.get("age")
        grade = request.POST.get("grade")
        gender = request.POST.get("gender")
        hobby = request.POST.getlist("hobby")
        Student(name=name, age=age, grade=grade, gender=gender, hobby=hobby).save()
        print(hobby)
        return redirect(reverse('student:list'))

def list(request):
    qs = Student.objects.all().order_by('-sno','name')
    return render(request,'student/list.html',{"list":qs})

def view(request, sno):
    qs = Student.objects.get(sno=sno)
    return render(request,'student/view.html',{"student":qs})