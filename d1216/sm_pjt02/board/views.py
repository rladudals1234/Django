from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import JsonResponse
from board.models import Board
from member.models import Member
from django.db.models import F, Q
from django.core.paginator import Paginator

# Create your views here.
# 게시판 리스트
def list(request):
    # 게시글 모두 가져오기
    qs = Board.objects.all().order_by('-bgroup','bstep')
    context = {'list':qs}
    # 하단 넘버링(1페이지에 10개씩)
    paginator = Paginator(qs, 10)   # 101 -> 11개
    page = int(request.GET.get('page', 1))   # 없으면 1페이지로
    list_qs = paginator.get_page(page)  # 1page -> 게시글 10개를 전달
    context['list'] = list_qs
    context['page'] = page  # 현재페이지 넘기기
    return render(request, 'board/list.html', context)

# 게시판 상세보기
def view(request, bno):
    # 게시글 가져오기
    qs = Board.objects.filter(bno=bno)
    # 조회를 한 후 조회된 데이터들을 update, delete : F
    # 조회수 1증가
    qs.update(bhit = F('bhit') + 1)
    context = {'board':qs[0]}
    return render(request, 'board/view.html', context)

# 게시판 글쓰기
def write(request):
    if request.method == 'GET':
        return render(request, 'board/write.html')
    elif request.method == 'POST':
        context = {'flag':'1'}
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        bfile = request.FILES.get('bfile','')
        id = request.session['session_id']
        member_qs = Member.objects.get(id=id)
        # bgroup값을 입력
        qs = Board.objects.create(btitle=btitle, bcontent=bcontent, bfile=bfile, member=member_qs)
        qs.bgroup = qs.bno
        qs.save()
        return render(request, 'board/write.html', context)

# 게시판 삭제
def delete(request, bno):
    qs = Board.objects.get(bno=bno)
    qs.delete()
    # context = {'flag':'2'}
    # return render(request, 'board/list.html', context)
    return redirect(reverse('board:list'))

# 게시판 수정
def update(request, bno):
    qs = Board.objects.get(bno=bno)
    context = {'board':qs}
    if request.method == 'GET':
        return render(request, 'board/update.html', context)
    elif request.method == 'POST':
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        bfile = request.FILES.get('bfile',qs.bfile)
        if bfile:
            qs.bfile = bfile
        qs.btitle = btitle
        qs.bcontent = bcontent
        id = request.session['session_id']
        qs.member = Member.objects.get(id=id)
        qs.save()
        context['flag']='1'
        # return render(request, 'board/update.html', context)
        return redirect(f'/board/view/{bno}/')