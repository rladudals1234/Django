from django.shortcuts import render,redirect
from django.urls import reverse
from member.models import Member
from django.http import HttpResponse, JsonResponse

# Create your views here.
# 로그인 부분
def login(request):
    if request.method == 'GET':
        cook_id = request.COOKIES.get("cook_id","")
        context = {'cook_id':cook_id}
        return render(request, 'member/login.html', context)
    elif request.method == 'POST':
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        qs = Member.objects.filter(id=id, pw=pw)
        context = {'redirect_url': reverse('member:login')}
        if qs:
            # session저장
            request.session['session_id'] = id
            request.session['session_name'] = qs[0].name
            context['state_code'] = "1"
        else:
            context['state_code'] = "0"
        login_keep = request.POST.get('login_keep')
        response = JsonResponse(context)
        # 쿠키저장
        if login_keep:
            response.set_cookie("cook_id", id, max_age=60*60*24*30)
        else:
            response.delete_cookie("cook_id")   # 쿠키 삭제
        return response

def logout(request):
    request.session.clear()
    return redirect(reverse('member:login'))