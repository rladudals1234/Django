from django.shortcuts import render, redirect
from django.http import JsonResponse
from customer.models import Board
from django.core.paginator import Paginator
from django.db.models import F, Q, Sum, Count
from member.models import Member
from comment.models import Comment
# get, post, put, delete방식 -> 지정
from rest_framework.decorators import api_view
# JsonResponse -> Response
from rest_framework.response import Response
# 상태값 출력
from rest_framework import status

# Create your views here.
def clist(request):
    # 검색부분---------------------------------------------
    category = request.GET.get('category','')
    search = request.GET.get('search','')
    print("검색으로 넘어온 데이터:",search)
    # ----------------------------------------------------
    if not search:
        qs = Board.objects.all().order_by('-bgroup','bstep')
    else:
        if category == 'btitle':
            qs = Board.objects.filter(btitle__contains=search).order_by('-bgroup','bstep')
        elif category == 'bcontent':
            qs = Board.objects.filter(bcontent__contains=search).order_by('-bgroup','bstep')
        elif category == 'all':
            qs = Board.objects.filter(Q(btitle__contains=search)|Q(bcontent__contains=search)).order_by('-bgroup','bstep')
    # Pagenator는 꼭 요청페이지 번호가 있어야 함.
    paginator = Paginator(qs,10)
    page = int(request.GET.get('page',1))
    list_qs = paginator.get_page(page)
    
    context = {'list':list_qs,'page':page, 'category':category, 'search':search}
    return render(request, 'customer/clist.html', context)

# 게시판 리스트 - GET방식으로 호출
@api_view(['GET'])
def clistJson(request):
    # print("페이지 번호", request.data.get('page',1))  # post방식
    # print("페이지 번호", request.GET.get('page',1))
    print("페이지 번호", request.query_params.get('page',1))
    qs = Board.objects.all().order_by('-bno')
    # Json형태로 전송하기 위해, list타입으로 변경
    l_qs = list(qs.values())
    context = {'list':l_qs}
    return Response(context, status=status.HTTP_200_OK)

@api_view(['GET'])
def cviewJson(request):
    bno = request.query_params.get('bno')
    qs = Board.objects.filter(bno=bno)
    l_qs = list(qs.values())
    context = {'result':l_qs[0]}
    return Response(context, status=status.HTTP_200_OK)

@api_view(['POST'])
def cwriteJson(request):
    id = request.data.get('id')
    btitle = request.data.get('btitle')
    bcontent = request.data.get('bcontent')
    member_qs = Member.objects.get(id=id)
    # db에 저장
    qs = Board.objects.create(btitle=btitle, bcontent=bcontent, member=member_qs)
    qs.bgroup = qs.bno
    qs.save()
    l_qs = list(Board.objects.filter(bno=qs.bno).values())
    context = {'result':'success', 'board':l_qs}
    return Response(context, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def cdeleteJson(request, bno):
    # bno = request.data.get('bno')
    name = request.data.get('name')
    print(name)
    # db에 저장
    qs = Board.objects.filter(bno=bno)
    qs.delete()
    context = {'result':'success'}
    return Response(context, status=status.HTTP_200_OK)

# 고객센터 페이지 뷰
# Board : 좋아요도 포함되어 전달됨.
def cview(request, bno):
    qs = Board.objects.get(bno=bno)
    # 이전글----------------------------------------------
    pre_qs = Board.objects.filter(Q(bgroup__lt=qs.bgroup) | Q(bgroup=qs.bgroup,bstep__gt=qs.bstep)).order_by('-bgroup','bstep').first()
    # 다음글----------------------------------------------
    # 답글달기가 포함되어 있을때 쿼리문
    next_qs = Board.objects.filter(Q(bgroup__gt=qs.bgroup) | Q(bgroup=qs.bgroup, bstep__lt=qs.bstep)).order_by('bgroup','-bstep').first()
    comment_qs = Comment.objects.filter(board=qs).order_by('-cno')
    context = {
        'c':qs,
        'pre_c':pre_qs,
        'next_c':next_qs,
        'comment_qs':comment_qs
    }
    return render(request, 'customer/cview.html', context)

def cwrite(request):
    if request.method == 'GET':
        return render(request, 'customer/cwrite.html')
    elif request.method == 'POST':
        id = request.session['session_id']
        btitle = request.POST.get('btitle')
        bcontent = request.POST.get('bcontent')
        bfile = request.FILES.get('bfile','')
        member_qs = Member.objects.get(id=id)
        # db에 저장
        qs = Board.objects.create(btitle=btitle, bcontent=bcontent, bfile=bfile, member=member_qs)
        qs.bgroup = qs.bno
        qs.save()
        return redirect('/customer/clist/')
    
def clikes(request):
    bno = request.POST.get('bno')
    board = Board.objects.get(bno=bno)
    id = request.session.get('session_id')
    member = Member.objects.get(id=id)
    
    # board.likes.all() : 게시글에 좋아요를 클릭한 회원
    # member.likes_member.all() : 현재회원이 좋아요를 클릭한 게시글 전체목록
    
    if board.likes.filter(pk=member.id).exists():
        # 제거
        board.likes.remove(member)  # likes안에 member를 제거
        like_chk = 0
    else:
        # 추가
        board.likes.add(member) # likes안에 member를 추가
        like_chk = 1
    count = board.likes.count() # 좋아요 개수
    print("좋아요 개수 확인",count)
        
    context={'result':'success', 'like_chk':like_chk, 'count':count}
    return JsonResponse(context)