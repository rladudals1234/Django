from django.shortcuts import render, redirect
from comment.models import Comment
from board.models import Board
from member.models import Member
from django.http import JsonResponse,HttpResponse    # 전송할때 json타입으로 변경해서 전송
from django.core import serializers     # Json타입으로 전달된 데이터를 파이썬데이터(set) 변경
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.
def list(request):
    # qs = list(Comment.objects.all().values())
    # for q in qs:
    #     q['cdate'] = q['cdate'].strftime('%Y-%m-%d')
    # return JsonResponse(qs, safe=False, encoder=DjangoJSONEncoder)
    
    # 첫번째 방식 - json형태로 반환
    # DateTimeField 타입, FileField 타입 -> 제대로 Json타입으로 변경이 안됨.
    bno=request.POST.get('bno')
    board_qs = Board.objects.get(bno=bno)
    qs = Comment.objects.filter(board=board_qs)
    list = serializers.serialize('json', qs)
    return HttpResponse(list, content_type="application/json")

    # 두번째 방식 위에서 qs까지 가져오기
    # context = {
    #     "list":serializers.serialize('json', qs),
    #     'flag':'success'
    # }
    # return JsonResponse(context)