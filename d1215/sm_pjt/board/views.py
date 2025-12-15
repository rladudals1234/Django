from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from board.models import Board
from member.models import Member
from django.db.models import F,Q

# Create your views here.
# 게시판 리스트
def list(request):
    qs = Board.objects.all().order_by('-bgroup','bstep')
    flag = request.GET.get('flag','')
    context = {'list':qs, 'flag':flag}
    return render(request, 'board/list.html', context)

# 글쓰기화면/글쓰기저장
def write(request):
    if request.method == 'GET':
        return render(request, 'board/write.html')
    elif request.method == 'POST':
        context = {'flag':'1'}
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        id = request.session['session_id']
        qs2 = Member.objects.get(id=id)
        qs = Board.objects.create(btitle=btitle, bcontent=bcontent, member=qs2)
        qs.bgroup = qs.bno
        qs.save()
        # return redirect(reverse('board:write'))
        return render(request, 'board/write.html', context)
    
def view(request, bno):
    qs = Board.objects.get(bno=bno)
    context = {'board':qs}
    return render(request, 'board/view.html', context)

def delete(request, bno):
    qs = Board.objects.get(bno=bno)
    qs.delete()
    return redirect(reverse('board:list'))

def update(request, bno):
    qs = Board.objects.get(bno=bno)
    context = {'board':qs}
    if request.method == 'GET':
        return render(request, 'board/update.html', context)
    elif request.method == 'POST':
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        qs.btitle = btitle
        qs.bcontent = bcontent
        id = request.session['session_id']
        qs.member = Member.objects.get(id=id)
        qs.save()
        context['flag']='1'
        # return render(request, 'board/update.html', context)
        return JsonResponse({'flag':'1', 'redirect_url': reverse('board:update', args=[qs.bno])})
    
# 답변달기
def reply(request, bno):
    qs = Board.objects.get(bno=bno)
    context = {'board':qs}
    if request.method == 'GET':
        return render(request, 'board/reply.html', context)
    elif request.method == 'POST':
        bgroup = int(request.POST.get('bgroup'))
        bstep = int(request.POST.get('bstep'))
        bindent = int(request.POST.get('bindent'))
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        id = request.session['session_id']
        qs2 = Member.objects.get(id=id)
        # 1. bgroup에서 부모보다 bstep이 높은값을 검색하고  (bstep_gt -> bstep<현재bstep)
        bstepup_qs = Board.objects.filter(bgroup=bgroup, bstep__gt=bstep)
        # 2. 검색된 데이터에서 bstep을 뽑아서 1씩 증가
        bstepup_qs.update(bstep=F('bstep')+1)
        # 답변달기 저장
        qs = Board.objects.create(btitle=btitle, bcontent=bcontent, member=qs2, bgroup=bgroup, bstep=bstep+1, bindent=bindent+1)
        context['flag']='2'
        # return redirect('board/list?flag=2')
        return render(request, 'board/reply.html', context)