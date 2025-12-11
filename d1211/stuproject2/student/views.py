from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from student.models import Student

# Create your views here.
def write(request):
    if request.method == 'GET':
        return render(request, 'student/write.html')
    elif request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        grade = request.POST.get('grade')
        gender = request.POST.get('gender')
        hobby = request.POST.getlist('hobby')
        qs = Student(name=name, age=age, grade=grade, gender=gender, hobby=hobby)
        qs.save()
        return redirect(reverse('student:list'))

def list(request):
    qs = Student.objects.all().order_by('-sno','name')
    context = {'list':qs}
    return render(request, 'student/list.html',context)

def view(request, sno):
    qs = Student.objects.get(sno=sno)
    context = {'stu':qs}
    return render(request, 'student/view.html', context)

def update(request, sno):
    qs = Student.objects.get(sno=sno)
    if request.method == 'GET':
        context = {'stu':qs}
        return render(request, 'student/update.html', context)
    elif request.method == 'POST':
        qs.name = request.POST.get('name')
        qs.age = request.POST.get('age')
        qs.grade = request.POST.get('grade')
        qs.gender = request.POST.get('gender')
        qs.hobby = request.POST.getlist('hobby')
        qs.save()
        return JsonResponse({'status': 'success', 'redirect_url': reverse('student:list')})
        # return redirect(reverse('student:list'))

def delete(request, sno):
    qs = Student.objects.get(sno=sno)
    qs.delete()
    # return redirect(reverse('student:list'))
    return JsonResponse({'status': 'success', 'redirect_url': reverse('student:list')})