from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from board.models import Board
from member.models import Member
from comment.models import Comment
from django.db.models import F, Q
from django.core.paginator import Paginator
import os
import uuid
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import urllib.parse
from board.forms import PostForm

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
    # 하단 댓글 - 해당 하단 댓글도 같이 가져올 수 있음 comment에 views에 clist의 ajax대신
    # c_qs = Comment.objects.filter(board=qs[0])  # ajax로 만들어 둔 것 대신 넘겨줄 수 있음
    # 조회를 한 후 조회된 데이터들을 update, delete : F
    # 조회수 1증가
    qs.update(bhit = F('bhit') + 1)
    context = {'board':qs[0]}
    return render(request, 'board/view.html', context)

def view2(request, bno):
    # 게시글 가져오기
    qs = Board.objects.filter(bno=bno)
    # 하단 댓글 - 해당 하단 댓글도 같이 가져올 수 있음 comment에 views에 clist의 ajax대신
    c_qs = Comment.objects.filter(board=qs[0]).order_by('-cno')  # ajax로 만들어 둔 것 대신 넘겨줄 수 있음
    qs.update(bhit = F('bhit') + 1)
    context = {'board':qs[0], 'clist':c_qs}
    return render(request, 'board/view2.html', context)

# 게시판 글쓰기
def write(request):
    if request.method == 'GET':
        form = PostForm()
        context = {'form':form}
        return render(request, 'board/write.html', context)
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
        form = PostForm(instance=qs)
        context['form'] = form
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

# 게시판 답글달기
def reply(request, bno):
    qs = Board.objects.get(bno=bno)
    context = {'board':qs}
    if request.method == 'GET':
        return render(request, 'board/reply.html', context)
    elif request.method == 'POST':
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        bgroup = int(request.POST.get('bgroup'))
        bstep = int(request.POST.get('bstep'))
        bindent = int(request.POST.get('bindent'))
        id = request.session['session_id']
        member_qs = Member.objects.get(id=id)
        bfile = request.FILES.get('bfile','')
        # 1. 답글달기 : 우선 같은 그룹에 있는 게시글의 bstep값을 1씩 먼저 증가
        board_qs = Board.objects.filter(bgroup=bgroup,bstep__gt = bstep)
        board_qs.update(bstep = F('bstep') + 1) # F함수 : 검색된 그 컬럼에만 값을 적용
        # 저장
        qs = Board.objects.create(btitle=btitle, bcontent=bcontent, bfile=bfile, member=member_qs, bgroup=bgroup, bstep=bstep+1, bindent=bindent+1)
        qs.save()
        context['flag']='2'
        # return render(request, 'board/update.html', context)
        return redirect(f'/board/reply/{bno}/', context)
    
def chart(request):
    return render(request, 'board/chart.html')

@csrf_exempt
def photoUpload(request):
    # HTML5 업로드
    file_name = request.headers.get('file-name')
    if not file_name:
        return HttpResponse("errstr=NoFileName", content_type="text/plain")

    ext = os.path.splitext(file_name)[-1]
    new_filename = f"{uuid.uuid4()}{ext}"

    upload_path = os.path.join(settings.MEDIA_ROOT, 'upload', new_filename)

    with open(upload_path, 'wb+') as f:
        f.write(request.body)
    
    file_url = request.build_absolute_uri(f"{settings.MEDIA_URL}upload/{new_filename}")
    
    response_content = f"sFileName={file_name}&sFileURL={file_url}&bNewline=true"
    return HttpResponse(response_content, content_type="text/plain; charset=utf-8")