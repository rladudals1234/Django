from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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

def list(request):
    qs = Member.objects.all().order_by('-mdate')
    paginator = Paginator(qs, 10)
    page = request.GET.get('page', 1) # GET 파라미터에서 'page' 값을 가져옴, 기본값은 1
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        # 페이지가 정수가 아닌 경우, 첫 페이지로 폴백
        list = paginator.page(1)
    except EmptyPage:
        # 페이지가 비어있는 경우(범위를 벗어난 경우), 마지막 페이지로 폴백
        list = paginator.page(paginator.num_pages)
    context = {
        'list': list,
        'page' : page
        }
    return render(request, 'member/board.html', context)