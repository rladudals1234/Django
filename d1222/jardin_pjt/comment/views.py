from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from comment.models import Comment
from customer.models import Board
from member.models import Member

# Create your views here.
def colist(request):
    # list타입으로 변경해서 json타입으로 변경을 해야 함.
    # objects.filter(), objects.all() -> list타입
    bno = request.GET.get('bno')
    board_qs = Board.objects.get(bno=bno)
    qs = Comment.objects.filter(board=board_qs)
    list_qs = list(qs.values())
    context = {'result':'success', 'list':list_qs}
    return JsonResponse(context)

def cowrite(request):
    bno = request.POST.get('bno')
    ccontent = request.POST.get('ccontent')
    cpw = request.POST.get('cpw')
    id = request.session['session_id']
    member_qs = Member.objects.get(id=id)
    board_qs = Board.objects.get(bno=bno)
    qs = Comment.objects.create(ccontent=ccontent, cpw=cpw, member=member_qs, board=board_qs)
    # 현재 사용자 말고도 중간에 다른 사용자가 등록할 경우도 생각해서 리스트 다시 불러오기(html에 ajax로 댓글리스트로 불러오는 함수(있는경우) 그대로 호출해서 사용가능)
    # 다른 사용자 등록까지 생각한 부분을 넣으려면 더보기나 페이징 등 그런 부분은 초기화됨(초기화 하지 않아도 될 때)
    # l_qs = list(Comment.objects.filter(cno=qs.cno).values())  # -> 속도는 빠름 다른사용자 갱신은 안됨
    l_qs = list(Comment.objects.filter(board=board_qs).order_by('-cno').values())
    # qs.save()
    context = {'result':'success', 'co':l_qs}
    return JsonResponse(context)

def codelete(request):
    cno = request.POST.get('cno')
    bno = request.POST.get('bno')
    qs = Comment.objects.filter(cno=cno)
    qs.delete()
    board_qs = Board.objects.get(bno=bno)
    l_qs = list(Comment.objects.filter(board=board_qs).order_by('-cno').values())
    # qs.save()
    context = {'result':'success', 'co':l_qs}
    return JsonResponse(context)

def coupdate(request):
    cno = request.POST.get('cno')
    cpw = request.POST.get('cpw')
    bno = request.POST.get('bno')
    ccontent = request.POST.get('ccontent')
    qs = Comment.objects.filter(cno=cno)
    qs.update(cpw=cpw, ccontent=ccontent)
    board_qs = Board.objects.get(bno=bno)
    l_qs = list(Comment.objects.filter(board=board_qs).order_by('-cno').values())
    # qs.save()
    context = {'result':'success', 'co':l_qs}
    return JsonResponse(context)