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
        # 쿠키 읽기
        cook_id = request.COOKIES.get("cook_id","")
        context = {"cook_id":cook_id}
        return render(request, 'member/login.html',context)
    elif request.method == 'POST':
        id = request.POST.get("id")
        pw = request.POST.get("pw")
        cook_keep = request.POST.get("cook_keep","")
        qs = Member.objects.filter(id=id, pw=pw)
        # qs = Member.objects.get(id=id, pw=pw).DoesNotExist()    # get은 이렇게해야 에러안남
        if qs:
            # request.session.session_id  # 세션불러오기
            # 세션 저장
            request.session['session_id'] = id
            
            # return redirect('/')
            context = {"error":"1", "msg":"로그인 성공"}
            response = render(request, 'member/login.html', context)
            # 쿠키저장, 삭제
            if cook_keep:
                response.set_cookie("cook_id", id, max_age=60*60*24*30)
            else:
                response.delete_cookie("cook_id")   # 쿠키 삭제
            
            return response
        else:
            context = {"error":"0", "msg":"아이디 또는 패스워드가 일치하지 않습니다."}
            return render(request, 'member/login.html', context)

def logout(request):
    # 세션 삭제
    request.session.clear() # 세션 모두 삭제
    # del request.session['session_id']
    context = {"error":"-1", "msg":"로그아웃"}
    return redirect('/member/login/')

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
