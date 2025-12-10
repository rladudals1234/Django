from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Student

# Create your views here.
def write(request):
    if request.method == 'GET':
        return render(request,'student/write.html')
    elif request.method == 'POST':
        # form에서 넘어온 데이터 처리
        name = request.POST.get("name")
        age = request.POST.get("age")
        grade = request.POST.get("grade")
        gender = request.POST.get("gender")
        hobby = request.POST.getlist("hobby")
        # hobbys = ",".join(hobby)  # 리스트타입을 문자열 타입으로 변환하는 방법
        # 리스트 타입을 문자항목에 저장하면 자동으로 형변환됨.
        Student(name=name, age=age, grade=grade, gender=gender, hobby=hobby).save()
        # Student(name=name, age=age, grade=grade, gender=gender).save()
        # print(request.POST.get("name"))
        # print(request.POST.get("age"))
        # print(request.POST.get("grade"))
        # print(request.POST.get("gender"))
        print(request.POST.getlist("hobby"))
        return redirect(reverse('student:list'))
        # return render(request,'student/write.html')
        # return redirect('/student/list/')

def list(request):
    qs = Student.objects.all().order_by('-sno','name')
    # qs = Student.objects.get(name='홍길동')
    # qs2 = Student.objects.get(name='유관순')
    # context = {"name":"홍길자", "student":qs, "student2":qs2}
    # return render(request,'student/list.html',context)
    # qs = Student.objects.all()
    context = {"list":qs}
    return render(request,'student/list.html',{"list":qs})

# def view(request):    # get방식
#     # request.GET["sno"]  # 데이터 없으면 에러
#     print("get방식 넘어온 데이터 sno : ",request.GET.get("sno"))
#     # print("넘어온 데이터 sno : ",sno)
#     return render(request,'student/view.html')

def view(request, sno, name):
    print("넘어온 데이터 sno : ",sno)
    print("넘어온 데이터 name : ",name)
    qs = Student.objects.get(sno=sno)
    return render(request,'student/view.html',{"student":qs})

def delete(request):
    return render(request,'student/delete.html')