from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from home.models import ChartData
from django.core import serializers

# Create your views here.
def index(request):
    return render(request, 'main.html')

def chart1(request):
    return render(request, 'chart1.html')

@csrf_exempt    # csrf_token 예외처리
def chart_json(request):
    request_data = request.GET.get('input_data','')
    if request_data:
        qs = ChartData.objects.filter(cyear=request_data)
    else:
        qs = ChartData.objects.all()
    context = {
        'dd_data':[10, 5, 9, 8, 3, 6],
        'll_data':['홍길동','유관순','이순신','강감찬','김구','김유신'],
        'list':list(qs.values())
    }
    return JsonResponse(context)

def chart2(request):
    return render(request, 'chart2.html')

def chart_json2(request):
    request_data = request.GET.get('input_data','')
    if request_data:
        qs = ChartData.objects.filter(cyear=request_data)
    else:
        qs = ChartData.objects.all()
    context = {
        'dd_data':[10, 5, 9, 8, 3, 6],
        'll_data':['홍길동','유관순','이순신','강감찬','김구','김유신'],
        'list':list(qs.values())
    }
    return JsonResponse(context)