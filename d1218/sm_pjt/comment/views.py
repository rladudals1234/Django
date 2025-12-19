from django.shortcuts import render, redirect
from comment.models import Comment
from board.models import Board
from member.models import Member
from django.http import JsonResponse    # 전송할때 json타입으로 변경해서 전송
from django.core import serializers     # Json타입으로 전달된 데이터를 파이썬데이터(set) 변경
import logging

logger = logging.getLogger('django')

# Create your views here.
# def clist(request):
#     bno=request.POST.get('bno')
#     board_qs = Board.objects.get(bno=bno)
#     qs = Comment.objects.filter(board=board_qs)
#     context = {
#         "list":serializers.serialize('json', qs),
#         'result':'success'
#     }
#     return JsonResponse(context)

# 하단댓글 부분 - 리턴타입이 Json형태로 변경해서 반환
def clist(request):
    try:
        bno=request.GET.get('bno')
        board_qs = Board.objects.get(bno=bno)
        # Json타입변경 - QuerySet List타입은 list타입으로 바로 변경
        qs = Comment.objects.filter(board=board_qs)
        list_qs = list(qs.values())  # QuerySet → 리스트 of dict
        context = {'result': 'success', 'list': list_qs}
        return JsonResponse(context)
    except Exception as e:
        logger.error("에러 : ", exc_info=True)

def cwrite(request):
    try:
        bno = request.POST.get('bno')
        ccontent = request.POST.get('ccontent')
        cpw = request.POST.get('cpw')
        id = request.session['session_id']
        member_qs = Member.objects.get(id=id)
        board_qs = Board.objects.get(bno=bno)
        qs = Comment.objects.create(ccontent=ccontent, cpw=cpw, member=member_qs, board=board_qs)
        qs.save()
        c_qs = list(Comment.objects.filter(cno=qs.cno).values())
        context = {'result':'success', 'c_comment':c_qs}
        return JsonResponse(context)
    except Exception as e:
        logger.error("에러 : ", exc_info=True)

def cdelete(request):
    try:
        cno = request.POST.get('cno')
        qs = Comment.objects.get(cno=cno)
        qs.delete()
        context = {'result':'success'}
        return JsonResponse(context)
    except Exception as e:
        logger.error("에러 : ", exc_info=True)

def cupdate(request):
    try:
        cno = request.POST.get('cno')
        ccontent = request.POST.get('ccontent')
        # qs = Comment.objects.get(cno=cno)
        # qs.ccontent = ccontent
        # qs.save()
        qs = Comment.objects.filter(cno=cno).update(ccontent=ccontent)
        c_qs = list(qs.values())
        context = {'result':'success', 'comment' : c_qs[0]}
        return JsonResponse(context)
    except Exception as e:
        logger.error("에러 : ", exc_info=True)