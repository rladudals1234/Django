from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.
def login(request):
    if request.method == 'GET':
        # 쿠키 검색
        cooksave_id = request.COOKIES.get("cooksave_id","") # 없으면 공백으로, get안쓰면 모두 읽어오기
        context = {"cooksave_id":cooksave_id}
        return render(request, 'member/login.html', context)
    elif request.method == 'POST':
        id = request.POST.get('id')
        pw = request.POST.get('pw')
        login_keep = request.POST.get('login_keep') # getlist()
        
        response = redirect("index")    # 앱이름으로 찾아감 /로 넣어도 됨
        if login_keep:
            print("아이디 저장이 체크가 되었습니다.")
            ## 쿠키에 아이디를 저장시켜줌
            response.set_cookie("cooksave_id", id, max_age=60*60*24*30)
        else:
            print("아이디 저장이 체크가 되지 않았습니다.")
            response.delete_cookie("cooksave_id")   # 쿠키 삭제
        return response