from api import models, serializers
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Area, LargeCategory, SmallCategory, MediumCategory, FootTraffic,MeanSale,MeanSaleRate, DevMeanSale,DevMeanSaleRate,recommendResult
from accounts.models import User
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from sklearn.metrics.pairwise import cosine_similarity
from .serializers import DevMeanSaleSerializer, DevMeanSaleRateSerializer
import pandas as pd
import requests
from django.forms.models import model_to_dict


@api_view(['GET'])
@permission_classes((AllowAny, ))
def dev_salerate(request, station_name):
    sales = DevMeanSale.objects.filter(area=station_name)
    l = []
    if len(sales)==0:
        return Response({'message': 'No station sale data', 'error':0})
    for sale in sales:
        l.append(
            model_to_dict(sale, fields=[field.name for field in sale._meta.fields])
        )
    sale_data = {}
    for idx, l_dict in enumerate(l):
        if not idx:
            for k, v in l_dict.items():
                if (k=='id')or(k=='area'):continue
                sale_data.update({k:v})
        else:
            for k, v in l_dict.items():
                if (k=='id')or(k=='area'):continue
                sale_data[k] += v
    for k, v in sale_data.items():
        sale_data[k] = v/(idx+1)

    rates = DevMeanSaleRate.objects.filter(area=station_name)
    l = []
    for rate in rates:
        l.append(
            model_to_dict(rate, fields=[field.name for field in sale._meta.fields])
        )        
    rate_data = {}
    for idx, l_dict in enumerate(l):
        if not idx:
            for k, v in l_dict.items():
                if (k=='id')or(k=='area'):continue
                rate_data.update({k:v})
        else:
            for k, v in l_dict.items():
                if (k=='id')or(k=='area'):continue
                rate_data[k] += v
    for k, v in rate_data.items():
        rate_data[k] = v/(idx+1)
    
    return Response({'rate': rate_data,'sale':sale_data})

def foottraffic(gu,dong):
    areas = Area.objects.filter(gu=gu, dong=dong)
    data = {
        'total' : 0,
        'men' : 0,
        'women' : 0,
        'teen':0,
        'twenty':0,
        'thirty':0,
        'fourty':0,
        'fifty':0,
        'sixty':0,
        'time1':0,
        'time2':0,
        'time3':0,
        'time4':0,
        'time5':0,
        'time6':0,
        'mon':0,
        'tue':0,
        'wed':0,
        'thr':0,
        'fri':0,
        'sat':0,
        'sun':0,
    }
    if not len(areas): return {'error':0,'message':'일치하는 유동인구 데이터가 없습니다.'}
    cnt = 0
    for area in areas:
        foot = area.foottraffic_set.all()
        if not foot: continue
        cnt += 1
        data['total'] += foot[0].total_pcnt
        data['men'] += foot[0].men_pcnt
        data['women'] += foot[0].women_pcnt
        data['teen'] += foot[0].teen_pcnt
        data['twenty'] += foot[0].twenty_pcnt
        data['thirty'] += foot[0].thirty_pcnt
        data['fourty'] += foot[0].fourty_pcnt
        data['fifty'] += foot[0].fifty_pcnt
        data['sixty'] += foot[0].sixty_pcnt
        data['time1'] += foot[0].time1_pcnt
        data['time2'] += foot[0].time2_pcnt
        data['time3'] += foot[0].time3_pcnt
        data['time4'] += foot[0].time4_pcnt
        data['time5'] += foot[0].time5_pcnt
        data['time6'] += foot[0].time6_pcnt
        data['mon'] += foot[0].mon_pcnt
        data['tue'] += foot[0].tue_pcnt
        data['wed'] += foot[0].wed_pcnt
        data['thr'] += foot[0].thr_pcnt
        data['fri'] += foot[0].fri_pcnt
        data['sat'] += foot[0].sat_pcnt
        data['sun'] += foot[0].sun_pcnt
    if not cnt: return {'error':0, 'message':'No Foottraffic Data !!!'}

    return data

def sales(gu, dong):
    sale_dict={
        'month' : 0,
        'week': 0,
        'weekend' : 0,
        'mon': 0,
        'tue': 0,
        'wed': 0,
        'thr': 0,
        'fri': 0,
        'sat': 0,
        'sun': 0,
        'time1' : 0,
        'time2' : 0,
        'time3' : 0,
        'time4' : 0,
        'time5' : 0,
        'time6' : 0,
        'men': 0,
        'women': 0,
        'teen' : 0,
        'twenty': 0,
        'thirty': 0,
        'fourty' : 0,
        'fifty': 0,
        'sixty': 0,
    }
    rate_dict = {
        'week': 0,
        'weekend' : 0,
        'mon': 0,
        'tue': 0,
        'wed': 0,
        'thr': 0,
        'fri': 0,
        'sat': 0,
        'sun': 0,
        'time1' : 0,
        'time2' : 0,
        'time3' : 0,
        'time4' : 0,
        'time5' : 0,
        'time6' : 0,
        'men': 0,
        'women': 0,
        'teen' : 0,
        'twenty': 0,
        'thirty': 0,
        'fourty' : 0,
        'fifty': 0,
        'sixty': 0,
    }
    
    areas = Area.objects.filter(gu=gu, dong=dong)
    if not len(areas): return {'error':0,'message':'지역과 일치하는 매출 데이터가 없습니다.'}
    cnt = 0
    for area in areas:
        sale = area.meansale_set.all()
        rate = area.meansalerate_set.all()
        if not sale: continue
        sale = sale[0]
        rate = rate[0]
        cnt += 1
        sale_dict['month'] += sale.month
        sale_dict['week'] += sale.week
        sale_dict['weekend'] += sale.weekend
        sale_dict['mon'] += sale.mon
        sale_dict['tue'] += sale.tue
        sale_dict['wed'] += sale.wed
        sale_dict['thr'] += sale.thr
        sale_dict['fri'] += sale.fri
        sale_dict['sat'] += sale.sat
        sale_dict['sun'] += sale.sun
        sale_dict['time1'] += sale.time1
        sale_dict['time2'] += sale.time2
        sale_dict['time3'] += sale.time3
        sale_dict['time4'] += sale.time4
        sale_dict['time5'] += sale.time5
        sale_dict['time6'] += sale.time6
        sale_dict['men'] += sale.men
        sale_dict['women'] += sale.women
        sale_dict['teen'] += sale.teen
        sale_dict['twenty'] += sale.twenty 
        sale_dict['thirty'] += sale.thirty
        sale_dict['fourty'] += sale.fourty
        sale_dict['fifty'] += sale.fifty
        sale_dict['sixty'] += sale.sixty

        rate_dict['week'] += rate.week
        rate_dict['weekend'] += rate.weekend
        rate_dict['mon'] += rate.mon
        rate_dict['tue'] += rate.tue
        rate_dict['wed'] += rate.wed
        rate_dict['thr'] += rate.thr
        rate_dict['fri'] += rate.fri
        rate_dict['sat'] += rate.sat
        rate_dict['sun'] += rate.sun
        rate_dict['time1'] += rate.time1
        rate_dict['time2'] += rate.time2
        rate_dict['time3'] += rate.time3
        rate_dict['time4'] += rate.time4
        rate_dict['time5'] += rate.time5
        rate_dict['time6'] += rate.time6
        rate_dict['men'] += rate.men
        rate_dict['women'] += rate.women
        rate_dict['teen'] += rate.teen
        rate_dict['twenty'] += rate.twenty 
        rate_dict['thirty'] += rate.thirty
        rate_dict['fourty'] += rate.fourty
        rate_dict['fifty'] += rate.fifty
        rate_dict['sixty'] += rate.sixty
    if not cnt: return {'error':0, 'message':'No Foottraffic Data !!!'}

    for k, v in sale_dict.items():
        sale_dict[k] = round(v/cnt,0)
    for k, v in rate_dict.items():
        rate_dict[k] = round(v/cnt, 0)
    data={
        'sale':sale_dict,
        'rate':rate_dict
    }
    return data


@api_view(['GET'])
@permission_classes((AllowAny, ))
def area_list(request, area_gu):
    print(request.data.get('gu'))
    areas = Area.objects.filter(gu=area_gu)
    dong = []
    for area in areas:
        if area.dong not in dong:
            dong.append(area.dong)
    return Response({'dong': dong})


@api_view(['GET'])
@permission_classes((AllowAny, ))
def category_list(request, medium):
    medium = medium.split(',')
    medium = '/'.join(medium)
    medium_category = MediumCategory.objects.filter(name=medium)
    small_category = SmallCategory.objects.filter(code__startswith=medium_category[0].code)
    small = [i.name for i in small_category]

    return Response({'small': small})

@api_view(['GET'])
@permission_classes((AllowAny, ))
def analyze(request, gu, dong):
    get_dong = Area.objects.filter(gu=gu, dong=dong)
    code = get_dong[get_dong.count()-1].dong_code
    base_url = "http://sg.sbiz.or.kr/areaGreadeDetail.json?admiCd="
    url = base_url + str(code)
    r = requests.get(url)
    to_json = r.json()['areaGrade']
    grothIndex = to_json['grothIndex']
    stability=to_json['stability']
    salePwr=to_json['salePwr']
    buyingPwr=to_json['buyingPwr']
    gathPwr=to_json['gathPwr']
    total_score = round((grothIndex + stability + salePwr + buyingPwr + gathPwr),1)

    if total_score >= 70:
        grade = 1
    elif total_score >= 57.5 and total_score < 70:
        grade = 2
    elif total_score >= 45 and total_score < 57.5:
        grade = 3
    elif total_score >= 32.5 and total_score < 45:
        grade = 4
    elif total_score < 32.5:
        grade = 5

    foot=foottraffic(gu,dong)
    sale=sales(gu,dong)
    data = {
        'scores': {
            'total_score': total_score,
            'grade': grade,
            'grothIndex':grothIndex,
            'stability':stability,
            'salePwr':salePwr,
            'buyingPwr':buyingPwr,
            'gathPwr':gathPwr
        },
        'foottraffic':foot,
        'sales': sale
    }

    return Response(data)

@api_view(['GET'])
@permission_classes((AllowAny, )) 
def user_analyze(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    area = user.interest_area.split()
    if user.interest_area == '':
        return Response({'message':'No InterestArea Data !!'})
    elif len(area) !=2:
        return Response({'message':'관심지역 저장이 이상해'})
    gu, dong = area[0], area[1]
    get_dong = Area.objects.filter(gu=gu, dong=dong)
    code = get_dong[get_dong.count()-1].dong_code
    base_url = "http://sg.sbiz.or.kr/areaGreadeDetail.json?admiCd="
    url = base_url + str(code)
    r = requests.get(url)
    to_json = r.json()['areaGrade']
    grothIndex = to_json['grothIndex']
    stability=to_json['stability']
    salePwr=to_json['salePwr']
    buyingPwr=to_json['buyingPwr']
    gathPwr=to_json['gathPwr']
    total_score = round((grothIndex + stability + salePwr + buyingPwr + gathPwr),1)

    if total_score >= 70:
        grade = 1
    elif total_score >= 57.5 and total_score < 70:
        grade = 2
    elif total_score >= 45 and total_score < 57.5:
        grade = 3
    elif total_score >= 32.5 and total_score < 45:
        grade = 4
    elif total_score < 32.5:
        grade = 5

    foot=foottraffic(gu,dong)
    sale=sales(gu,dong)
    data = {
        'scores': {
            'total_score': total_score,
            'grade': grade,
            'grothIndex':grothIndex,
            'stability':stability,
            'salePwr':salePwr,
            'buyingPwr':buyingPwr,
            'gathPwr':gathPwr
        },
        'foottraffic':foot,
        'sales': sale
    }

    return Response(data)

@api_view(['GET'])
@permission_classes((AllowAny, ))
def recommend(request, gu,dong):
    result = recommendResult.objects.filter(gu=gu,dong=dong)
    return Response(result[0].result)