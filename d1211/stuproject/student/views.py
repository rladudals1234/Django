from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from student.models import Student

# Create your views here.
# 학생등록페이지
def write(request):
    if request.method == 'GET':
        return render(request,'student/write.html')
    elif request.method == 'POST':
        # sno = request.POST.get("sno")
        name = request.POST.get("name")
        age = request.POST.get("age")
        grade = request.POST.get("grade")
        gender = request.POST.get("gender")
        hobby = request.POST.getlist("hobby")
        qs = Student(name=name, age=age, grade=grade, gender=gender, hobby=hobby)
        qs.save()
        # txt = f"{name},{age},{grade},{gender},{hobby}"
        # print(txt)
        # return HttpResponse("post입력됨")
        # return render(request,'student/list.html')  # redirect로 해야 주소가 바뀜 redirect 안하면 계속 등록되거나 기존 페이지로 오게됨
        return redirect(reverse('student:list'))

# 학생리스트페이지
def list(request):
    qs = Student.objects.all().order_by('-sno','name')
    context = {'list':qs}
    context['test'] = 'aaa'
    return render(request,'student/list.html',context)

# 학생상세보기페이지
def view(request, sno):
    qs = Student.objects.get(sno=sno)
    context = {'stu':qs}
    return render(request,'student/view.html',context)

# 학생수정
def update(request, sno):
    qs = Student.objects.get(sno=sno)
    context = {'stu':qs}
    if request.method == 'GET':
        return render(request,'student/update.html', context)
    elif request.method == 'POST':
        qs.name = request.POST.get("name")
        qs.age = request.POST.get("age")
        qs.grade = request.POST.get("grade")
        qs.gender = request.POST.get("gender")
        qs.hobby = request.POST.getlist("hobby")
        qs.save()
        # txt = f"{name},{age},{grade},{gender},{hobby}"
        # print(txt)
        # return HttpResponse("post입력됨")
        # return render(request,'student/list.html')  # redirect로 해야 주소가 바뀜 redirect 안하면 계속 등록되거나 기존 페이지로 오게됨
        return redirect(reverse('student:list'))

# 학생삭제
def delete(request, sno):
    qs = Student.objects.get(sno=sno)
    qs.delete()
    return redirect(reverse('student:list'))