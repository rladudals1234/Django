from django.shortcuts import render, redirect
from customer.models import Board
from django.core.paginator import Paginator
from django.db.models import F, Q, Sum, Count
from member.models import Member

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

def cview(request, bno):
    qs = Board.objects.get(bno=bno)
    # 이전글----------------------------------------------
    pre_qs = Board.objects.filter(Q(bgroup__lt=qs.bgroup) | Q(bgroup=qs.bgroup,bstep__gt=qs.bstep)).order_by('-bgroup','bstep').first()
    # 다음글----------------------------------------------
    # 답글달기가 포함되어 있을때 쿼리문
    next_qs = Board.objects.filter(Q(bgroup__gt=qs.bgroup) | Q(bgroup=qs.bgroup, bstep__lt=qs.bstep)).order_by('bgroup','-bstep').first()
    context = {
        'c':qs,
        'pre_c':pre_qs,
        'next_c':next_qs
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