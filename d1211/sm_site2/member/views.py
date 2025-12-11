from django.shortcuts import render, redirect
from django.urls import reverse
from member.models import Member

# Create your views here.
def login(request):
    if request.method=='GET':
        return render(request,'member/login.html')
    elif request.method=='POST':
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        qs = Member.objects.filter(id=id, pw=pw)
        if qs:
            return redirect(reverse('member:list'))
        else:
            return redirect(reverse('member:login'))

def write(request):
    if request.method=='GET':
        return render(request,'member/write.html')
    elif request.method=='POST':
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        hobby = request.POST.getlist('hobby')
        Member.objects.create(id=id, pw=pw, name=name, phone=phone, gender=gender, hobby=hobby)
        return redirect(reverse('member:write'))

def list(request):
    qs = Member.objects.all().order_by('-mdate')
    context = {'list':qs}
    return render(request,'member/list.html',context)