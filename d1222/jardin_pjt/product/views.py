from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import requests
from django.conf import settings
import json

# Create your views here.
# 제품상세페이지
def detail(request):
    return render(request, 'product/detail.html')

kakao_api_key = 'DEV안보이게'
kakaopay_url = 'https://open-api.kakaopay.com/online/v1/payment/ready'

# 카카오페이 준비화면
def prepare_payment(request):
    # 상품명, 판매가, 수량 정보를 가져옴.
    headers = {
        'Authorization':f'SECRET_KEY {kakao_api_key}',
        'Content-Type':'application/json'
    }
    # 결제정보
    data = {
        "cid": "TC0ONETIME",                                        # 가맹점코드 - 테스트버전
		"partner_order_id": "partner_order_id",                     # 가맹점 주문번호
		"partner_user_id": "partner_user_id",                       # 가맹점 회원id
		"item_name": "쟈뎅 오리지널 콜롬비아 페레이라 원두커피백 15p",      # 상품명
		"quantity": "1",                                            # 수량
		"total_amount": "4330",                                     # 금액
		"vat_amount": "433",                                        # 상품 부가세 금액
		"tax_free_amount": "0",                                     # 상품 비과세 금액
		"approval_url": "http://localhost:8000/product/approve",     # 결제 성공 시 redirect url, 최대 255자
		"fail_url": "http://localhost:8000/product/fail",            # 결제 실패 시 redirect url, 최대 255자
		"cancel_url": "http://localhost:8000/product/cancel"         # 결제 취소 시 redirect url, 최대 255자
    }
    # requests -> url에 있는 데이터 전송, 응답
    # request, response -> 브라우저에서 페이지를 열때 전달되는 객체
    response = requests.post(kakaopay_url, headers=headers, data=json.dumps(data,ensure_ascii=False))
    # 리턴받은 정보 - json으로 변환
    # 5개 : 결제고유번호, 앱일때, 모바일일때, pc일때, 결제 준비 요청 시간
    result = response.json()
    print("리턴받은결과 : ",result)
    # 섹션저장 - 결제 고유 번호
    request.session['tid'] = result['tid']
    request.session['order_id'] = data['partner_order_id']
    # 결제창을 넘겨줌.
    print("결제창화면 : ",result['next_redirect_pc_url'])
    
    if response.status_code == 200: # 성공일때
        return redirect(result['next_redirect_pc_url'])
    else:
        return redirect("/product/fail/")

# 카카오페이 결제승인창
def approve(request):
    # 리턴받은 값
    pg_token = request.GET.get('pg_token')
    tid = request.session.get("tid")
    order_id = request.session.get("order_id")
    print("리턴받은값 : ", pg_token,tid,order_id)
    if not pg_token or not tid:
        return redirect("/product/fail/")
    url = 'https://open-api.kakaopay.com/online/v1/payment/approve'
    headers = {
        'Authorization':f'SECRET_KEY {kakao_api_key}',
        'Content-Type':'application/json'
    }
    data = {
		"cid": "TC0ONETIME",
		"tid": tid,
		"partner_order_id": order_id,
		"partner_user_id": "partner_user_id",
		"pg_token": pg_token
	}
    response = requests.post(url, headers=headers, data=json.dumps(data,ensure_ascii=False))
    print("리턴받은 결과 : ",response)
    result = response.json()
    print("결제날짜 : ",result['created_at'])
    if result.get('aid'):
        # DB에 저장 - 결제정보
        # 결제정보.objects.create()
        print("결제성공!!!")
        return redirect("/product/success/")
    
    return redirect("/product/fail/")

# 카카오페이 성공
def success(request):
    return HttpResponse("결제 성공")

# 카카오페이 실패
def fail(request):
    return HttpResponse("결제 실패")

# 카카오페이 취소
def cancel(request):
    return HttpResponse("결제 취소")
