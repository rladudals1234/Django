from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json
from member.models import Member

# Create your views here.

def step03(request):
    return render(request, 'step03.html')

def idCheck(request):
    id = request.POST.get("id")
    qs = Member.objects.filter(id=id)
    if not qs:
        result = "사용가능"
    else:
        result = "사용불가"
    context = {
               'resultCode':'success', 
               'result':qs.exists()
    }
    return JsonResponse(context)

def userAll(request):
    id = request.GET.get("id","")
    name = request.GET.get("name","")
    qs = Member.objects.all()
    l_qs = list(qs.values())
    context = {
        'resultCode':'success', 
        'list':l_qs
    }
    return JsonResponse(context)

def userInsert(request):
    # id = request.POST.get("id","")
    # name = request.POST.get("name","")
    body = json.loads(request.body)     # post는 변환해서
    id = body.get('id')
    name = body.get('name')
    qs = Member.objects.all()
    l_qs = list(qs.values())
    context = {
        'resultCode':'success', 
        'list':l_qs
    }
    return JsonResponse(context)

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        id = request.POST.get("id")
        pw = request.POST.get("pw")
        qs = Member.objects.filter(id=id, pw=pw)
        if qs.exists():
            result = "success"
            request.session['session_id'] = id
            request.session['session_name'] = qs[0].name
        else:
            result = "fail"
        context = {'resultCode':result}
        return JsonResponse(context)
    
def logout(request):
    # 세션 모두 삭제
    request.session.clear()
    context = {"msg":"로그아웃"}
    return redirect('/')
    # return JsonResponse(context)