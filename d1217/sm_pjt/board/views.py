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

# @csrf_exempt
# def photoUpload(request):
#     # 1. 파일 데이터 파악
#     file_data = request.FILES.get('Filedata')
    
#     if file_data:
#         # [방식 1] 일반 폼 업로드 (구형 브라우저 또는 단일 업로드)
#         file_name = file_data.name
#         ext = os.path.splitext(file_name)[-1]
#         new_filename = f"{uuid.uuid4()}{ext}"
        
#         upload_path = os.path.join(settings.MEDIA_ROOT, 'upload', new_filename)
#         with open(upload_path, 'wb+') as destination:
#             for chunk in file_data.chunks():
#                 destination.write(chunk)
        
#         # 콜백 처리
#         callback = request.GET.get('callback') or '/static/smarteditor2-2.8.2.3/sample/photo_uploader/callback.html'
#         callback_func = request.GET.get('callback_func')
#         file_url = f"{settings.MEDIA_URL}upload/{new_filename}"
        
#         response_url = f"{callback}?callback_func={callback_func}&sFileName={new_filename}&sFileURL={file_url}&bNewline=true"
#         return redirect(response_url)

#     else:
#         # [방식 2] HTML5 다중 업로드
#         file_name = request.headers.get('file-name') or request.GET.get('sFileName')
#         if not file_name:
#             return HttpResponse("errstr=NoFileName") # 에러 시에도 형식을 맞춰야 함

#         ext = os.path.splitext(file_name)[-1]
#         new_filename = f"{uuid.uuid4()}{ext}"
        
#         upload_path = os.path.join(settings.MEDIA_ROOT, 'upload', new_filename)
        
#         with open(upload_path, 'wb+') as destination:
#             destination.write(request.body)
            
#         # [중요] 도메인을 포함한 전체 URL을 보내야 안전합니다.
#         file_url = request.build_absolute_uri(f"{settings.MEDIA_URL}upload/{new_filename}")
        
#         # [수정 핵심] callback URL을 포함하지 말고, 순수 데이터만 반환하세요.
#         # 이 응답을 Ajax가 받아서 에디터에 직접 삽입합니다.
#         # 콜백 처리
#         callback = request.GET.get('callback') or '/static/smarteditor2-2.8.2.3/sample/photo_uploader/callback.html'
#         callback_func = request.GET.get('callback_func')
#         return HttpResponse(f"{callback}?callback_func={callback_func}&sFileName={new_filename}&sFileURL={file_url}&bNewline=true")

@csrf_exempt
def photoUpload(request):
    # 1. 파일 데이터 파악
    file_data = request.FILES.get('Filedata')
    
    if file_data:
        # [방식 1] 일반 폼 업로드 (구형 브라우저 또는 단일 업로드)
        file_name = file_data.name
        ext = os.path.splitext(file_name)[-1]
        new_filename = f"{uuid.uuid4()}{ext}"
        
        upload_path = os.path.join(settings.MEDIA_ROOT, 'upload', new_filename)
        with open(upload_path, 'wb+') as destination:
            for chunk in file_data.chunks():
                destination.write(chunk)
        
        # 콜백 처리
        callback = request.GET.get('callback') or '/static/smarteditor2-2.8.2.3/sample/photo_uploader/callback.html'
        callback_func = request.GET.get('callback_func')
        file_url = f"{settings.MEDIA_URL}upload/{new_filename}"
        
        response_url = f"{callback}?callback_func={callback_func}&sFileName={new_filename}&sFileURL={file_url}&bNewline=true"
        return redirect(response_url)
    else:
        # HTML5 업로드
        file_name = request.headers.get('file-name')
        if not file_name:
            return HttpResponse("errstr=NoFileName", content_type="text/plain")

        ext = os.path.splitext(file_name)[-1]
        new_filename = f"{uuid.uuid4()}{ext}"

        upload_path = os.path.join(settings.MEDIA_ROOT, 'upload', new_filename)

        with open(upload_path, 'wb+') as f:
            f.write(request.body)

        file_url = request.build_absolute_uri(
            f"{settings.MEDIA_URL}upload/{new_filename}"
        )

        # 이 형식만 반환해야 함
        response =  HttpResponse(
            "sFileName={}\n"
            "&sFileURL={}\n"
            "&bNewline=true".format(new_filename, file_url),
            content_type="text/html; charset=utf-8"
        )
        response["Content-Type"] = "text/html; charset=utf-8"
        response["Cache-Control"] = "no-cache"
        return response