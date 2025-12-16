from django.shortcuts import render,redirect
from django.urls import reverse
from board.models import Board
import datetime

# Create your views here.

# 게시글 작성
def write(request):
    if request.method == 'GET':
        return render(request, 'board/write.html')
    elif request.method == 'POST':
        btitle = request.POST.get('btitle')
        bfile = request.FILES.get('bfile')  # file타입이기에 FILES로 읽어야 함.
        print("날짜 : ", datetime.datetime.now())
        print("날짜 : ", datetime.datetime.now().microsecond)
        bfile.name = f'{datetime.datetime.now().microsecond}_{bfile.name}'  # 이름변경해서 저장가능
        
        # 파일저장
        qs = Board.objects.create(btitle=btitle, bfile=bfile)
        qs.save()
        return render(request, 'board/write.html')
        # return redirect(reverse('board:write'))