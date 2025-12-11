from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .models import Member

# Create your views here.
# 회원전체리스트페이지
def list(request):
    qs = Member.objects.all().order_by('-mdate')
    context = {'list':qs}
    return render(request, 'member/list.html', context)

# 로그인
def login(request):
    if request.method == 'GET':
        return render(request, 'member/login.html')
    elif request.method == 'POST':
        id = request.POST.get("id")
        pw = request.POST.get("pw")
        qs = Member.objects.filter(id=id, pw=pw)
        if qs:
            return redirect('/')
        else:
            context = {"error":"0", "msg":"아이디 또는 패스워드가 일치하지 않습니다."}
            return render(request, 'member/login.html', context)

def view(request, id):
    qs = Member.objects.get(id=id)
    context = {'member':qs}
    return render(request, 'member/view.html', context)

# 회원등록페이지
def write(request):
    if request.method == 'GET':
        return render(request, 'member/write.html')
    elif request.method == 'POST':
        id = request.POST.get("id")
        pw = request.POST.get("pw")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        gender = request.POST.get("gender")
        hobby = request.POST.get("hobby")
        Member.objects.create(id=id, pw=pw, name=name, phone=phone, gender=gender, hobby=hobby)
        # qs = Member(id=id, pw=pw, name=name, phone=phone, gender=gender, hobby=hobby)
        # qs.save()
        return redirect('/member/write/')
        # return HttpResponse("post입력")
