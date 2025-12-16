from django.shortcuts import render
from member.models import Member

# Create your views here.
# 로그인
def login(request):
    if request.method == 'GET':
        return render(request, 'member/login.html')

    elif request.method == 'POST':
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        qs = Member.objects.filter(id=id, pw=pw)
        context = {}
        if qs:
            request.session['session_id'] = id
            request.session['session_name'] = qs[0].name
            context = {'flag':'1'}
        else:
            context = {
                'flag':'0',
                'id':id,
                'pw':pw
                }
        
        return render(request, 'member/login.html', context)
    
# 로그아웃
def logout(request):
    request.session.clear()
    context = {'flag':'-1'}
    return render(request, 'member/login.html',context)