from django.shortcuts import render

# Create your views here.
def index(request):
    # 쿠키 읽어오기 - request
    # 쿠키 저장 - response
    
    # 쿠키 검색
    cook_info = request.COOKIES
    print("쿠키모든정보 : ", cook_info)
    cook_id = request.COOKIES.get("cook_id","")    # 쿠키가져오며 쿠키가 없을때 빈공백
    print("cook_id 정보 : ", cook_id)
    
    ## 쿠키저장 - response
    response = render(request, 'index.html')
    # 쿠키정보가 없을때만 쿠키 저장
    # if not cook_id:
    #     response.set_cookie("smsite_connect", "ok")
    #     # 유지시간 없으면 브라우저 종료시 사라짐, 시간을 설정하면 시간동안 유지
    #     response.set_cookie("ip", "127.0.0.1", max_age=60*60*24)    # 60초*60분*24시간=1일
    # else:
    #     print("쿠키를 저장하지 않습니다.")
    return response