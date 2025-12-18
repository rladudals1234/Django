from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from board.models import Board
from member.models import Member
from comment.models import Comment
from django.db.models import F, Q
from stuscore.models import Stuscore

# Create your views here.
def slist(request):
    if request.method == 'POST':
        no = int(request.POST.get("no"))
        qs = Stuscore.objects.all().order_by('sno')[no:(no+5)]
        list_qs = list(qs.values())  # QuerySet → 리스트
        context = {'result': 'success','list':list_qs}
        return JsonResponse(context)