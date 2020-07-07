import json
import pandas as pd
import os
import shutil
import datetime
import requests

DATA_DIR = "../data"
DATA_FILE = os.path.join(DATA_DIR, "data.json")
DUMP_FILE = os.path.join(DATA_DIR, "dump.pkl")

store_columns = (
    "id",  # 음식점 고유번호
    "store_name",  # 음식점 이름
    "branch",  # 음식점 지점 여부
    "area",  # 음식점 위치
    "tel",  # 음식점 번호
    "address",  # 음식점 주소
    "latitude",  # 음식점 위도
    "longitude",  # 음식점 경도
    "category",  # 음식점 카테고리
    'review_count',
    
)

menu_columns = (
    'id',
    'store',
    'menu_name',
    'price',
)

user_columns = (
    'id',
    'gender',
    'age',
)

review_columns = (
    "id",  # 리뷰 고유번호
    "store",  # 음식점 고유번호
    "user",  # 유저 고유번호
    "score",  # 평점
    "content",  # 리뷰 내용
    "reg_time",  # 리뷰 등록 시간
)

def pointRegion(code):
    base_url = "http://sg.sbiz.or.kr/areaGreadeDetail.json?admiCd="
    url = base_url + str(code)
    r = requests.get(url)
    to_json = r.json()['areaGrade']
    total_score = 0
    grade = 0
    grothIndex = 0
    stability = 0
    salePwr = 0
    buyingPwr = 0
    gathPwr = 0
    if to_json :
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
    return {'total_score': total_score,'grade': grade,'grothIndex':grothIndex,
            'stability':stability,'salePwr':salePwr,'buyingPwr':buyingPwr,'gathPwr':gathPwr}

def similarPoint(score, review):
    result ={}
    point = 10
    for i, val in score.iterrows():
        now_key = val.medium_category
        if now_key in result.keys():
            result[now_key] += point
        else:
            result[now_key] = point
        point -= 1
    point = 10
    for i, val in review.iterrows():
        now_key = val.medium_category
        if now_key in result.keys():
            result[now_key] += point
        else:
            result[now_key] = point
        point -= 1
    
    result = sorted(result.items(),reverse=True,key=lambda item: item[1])
    return result

def onePlusTen(score, review):
    result ={}
    point = 1
    for i, val in score.iterrows():
        now_key = val.medium_category
        if now_key in result.keys():
            result[now_key] += point
        else:
            result[now_key] = point
        point += 1
    point = 10
    for i, val in review.iterrows():
        now_key = val.medium_category
        if now_key in result.keys():
            result[now_key] += point
        else:
            result[now_key] = point
        point -= 1
    
    return result

def tenPlusTen(score, review):
    result ={}
    point = 10
    for i, val in score.iterrows():
        now_key = val.medium_category
        if now_key in result.keys():
            result[now_key] += point
        else:
            result[now_key] = point
        point -= 1
    point = 10
    for i, val in review.iterrows():
        now_key = val.medium_category
        if now_key in result.keys():
            result[now_key] += point
        else:
            result[now_key] = point
        point -= 1
    
    return result

def onePlusOne(score, review):
    result ={}
    point = 1
    for i, val in score.iterrows():
        now_key = val.medium_category
        if now_key in result.keys():
            result[now_key] += point
        else:
            result[now_key] = point
        point += 1
    point = 1
    for i, val in review.iterrows():
        now_key = val.medium_category
        if now_key in result.keys():
            result[now_key] += point
        else:
            result[now_key] = point
        point += 1
    
    return result

def tenPlusOne(score,review):
    result ={}
    point = 10
    for i, val in score.iterrows():
        now_key = val.medium_category
        if now_key in result.keys():
            result[now_key] += point
        else:
            result[now_key] = point
        point -= 1
    point = 1
    for i, val in review.iterrows():
        now_key = val.medium_category
        if now_key in result.keys():
            result[now_key] += point
        else:
            result[now_key] = point
        point += 1
    
    return result

def recommendResult(similar, ot, tt, oo, to):
    result = {'top':[],'ot':[], 'tt':[],'oo':[],'to':[]}

    # top
    top = 0
    for key, value in similar:
        if top == 3:
            break
        if key not in ot.keys():
            result['top'].append(key)
        top += 1
    if len(ot) > 0:
        # 1
        for key, value in ot.items():
            for k, v in similar:
                if key == k:
                    ot[key] = value * v
        sorted_ot = sorted(ot.items(),reverse=True,key=lambda item: item[1])

        # 2
        for key, value in tt.items():
            for k, v in similar:
                if key == k:
                    tt[key] = value * v
        sorted_tt = sorted(tt.items(),reverse=True,key=lambda item: item[1])

        # 3
        for key, value in oo.items():
            for k, v in similar:
                if key == k:
                    oo[key] = value * v
        sorted_oo = sorted(oo.items(),reverse=True,key=lambda item: item[1])

        # 4
        for key, value in to.items():
            for k, v in similar:
                if key == k:
                    to[key] = value * v
        sorted_to = sorted(to.items(),reverse=True,key=lambda item: item[1])

        ot_max = sorted_ot[0][1]
        for i in sorted_ot:
            if i[1] == ot_max:
                result['ot'].append(i[0])
            else :
                break
        tt_max = sorted_tt[0][1]
        for i in sorted_tt:
            if i[1] == tt_max:
                result['tt'].append(i[0])
            else :
                break
        oo_max = sorted_oo[0][1]
        for i in sorted_oo:
            if i[1] == oo_max:
                result['oo'].append(i[0])
            else :
                break
        to_max = sorted_to[0][1]
        for i in sorted_to:
            if i[1] == to_max:
                result['to'].append(i[0])
            else :
                break

    return result

import json
def recommend(data, gu, dong):
    cluster = data['similarity']
    cluster_number = cluster.loc[(cluster['gu'] == gu) & (cluster['dong'] == dong), :]['predict'].values[0]

    # 입력받은 행정동 지역과 유사한(같은 클러스터)의 지역 리스트 확인
    similar_region = cluster.loc[(cluster['predict'] == cluster_number),['gu','dong']]
    
    stores_reviews_merge = pd.merge(data['stores'], data['reviews'], left_on="id", right_on="store")
    stores_reviews_merge = stores_reviews_merge.loc[:,['gu','dong','medium_code','small_code','score','store','store_name','user','content']]

    # 유사 지역의 모든 음식점의 리뷰데이터
    similar_stores_df = pd.DataFrame(columns=['gu','dong','medium_code','small_code','score','store','store_name','user','content'])
    for i, val in similar_region.iterrows():
        now_gu = val.gu
        now_dong = val.dong
        similar_region_stores = stores_reviews_merge.loc[(stores_reviews_merge['gu'] == now_gu) & (stores_reviews_merge['dong'] == now_dong),:]
        similar_stores_df = pd.concat([similar_stores_df, similar_region_stores], ignore_index=True)
    similar_stores_df['score'] = similar_stores_df.score.astype(int)

    similar_groupby_small_code = similar_stores_df.groupby(['medium_code'])
    similar_scores_small_code = similar_groupby_small_code.mean()
    similar_scores_small_code['count'] = similar_groupby_small_code.count()['content']
    similar_scores_small_code = similar_scores_small_code.loc[similar_scores_small_code['count']>=3]

    # 평점으로 뽑아보기
    similar_scores_small_code_sort_by_score = pd.merge(similar_scores_small_code, data['medium'], on="medium_code").sort_values(by="score", ascending=False)[0:10].reset_index()
    # 리뷰수로 뽑아보기
    similar_scores_small_code_sort_by_count =  pd.merge(similar_scores_small_code, data['medium'], on="medium_code").sort_values(by="count", ascending=False)[0:10].reset_index()
    
    
    #선택 지역
    region_stores = stores_reviews_merge.loc[(stores_reviews_merge['gu'] == gu) & (stores_reviews_merge['dong'] == dong),['medium_code','score','content']]

    region_groupby_small_code =region_stores.groupby(['medium_code'])
    region_scores_small_code = region_groupby_small_code.mean()
    region_scores_small_code['count'] = region_groupby_small_code.count()['content']
    region_scores_small_code = region_scores_small_code.loc[region_scores_small_code['count']>=3]

    # 평점으로 뽑아보기
    region_scores_small_code_sort_by_score = pd.merge(region_scores_small_code, data['medium'], on="medium_code").sort_values(by="score", ascending=False)[0:10].reset_index()
    # 리뷰수로 뽑아보기
    region_scores_small_code_sort_by_count =  pd.merge(region_scores_small_code, data['medium'], on="medium_code").sort_values(by="count", ascending=False)[0:10].reset_index()
    
    ret = {}
    
    if similar_scores_small_code.size > 0:
        similar_point = similarPoint(similar_scores_small_code_sort_by_score, similar_scores_small_code_sort_by_count)
        one_plus_ten = onePlusTen(region_scores_small_code_sort_by_score,region_scores_small_code_sort_by_count)
        ten_plus_ten = tenPlusTen(region_scores_small_code_sort_by_score,region_scores_small_code_sort_by_count)
        one_plus_one = onePlusOne(region_scores_small_code_sort_by_score,region_scores_small_code_sort_by_count)
        ten_plus_one = tenPlusOne(region_scores_small_code_sort_by_score,region_scores_small_code_sort_by_count)

        result = recommendResult(similar_point,one_plus_ten,ten_plus_ten,one_plus_one,ten_plus_one)

        ret = {
            'similar_scores_small_code_sort_by_score':json.loads(similar_scores_small_code_sort_by_score.to_json(orient='table',force_ascii=False)),
            'similar_scores_small_code_sort_by_count':json.loads(similar_scores_small_code_sort_by_count.to_json(orient='table',force_ascii=False)),
            'region_scores_small_code_sort_by_score':json.loads(region_scores_small_code_sort_by_score.to_json(orient='table',force_ascii=False)),
            'region_scores_small_code_sort_by_count':json.loads(region_scores_small_code_sort_by_count.to_json(orient='table',force_ascii=False)),
            'recommend' : result
        }
    
    return ret
    
def allRecommend(data):
    similarity = data['similarity']
    result = []
    for i, val in similarity.iterrows():
        res= {}
        res['gu'] = val.gu
        res['dong'] = val.dong
        res['result'] = recommend(data, val.gu, val.dong)
        result.append(res)
    
    return result

def foottraffic(data, gu, dong):
    areas = data['area'].loc[(data['area']['gu'] == gu) & (data['area']['dong'] == dong),:]['road_name']
    ret = {
        'total' : 0,
        'men' : 0,
        'women' : 0,
        'teen':0,
        'twenty':0,
        'thirty':0,
        'fourty':0,
        'fifty':0,
        'sixty':0,
    }
    roads = data['population'].loc[data['population']['road'].isin(areas)]
    if roads.size == 0:
        return ret
    # 순서를 메기자 1이 더 높은거!
    else:
        roads = roads.groupby(['year','quarter']).sum().reset_index()
        ret['total'] = roads.loc[:,'total_pcnt'].values[0]
        men = roads.loc[:,'men_pcnt'].values[0]
        women = roads.loc[:,'women_pcnt'].values[0]
        if men > women :
            ret['men'] = 1
            ret['women'] = 2
        else:
            ret['men'] = 2
            ret['women'] = 1

        age_value = []
        age_columns = ["teen","twenty","thirty","fourty","fifty","sixty"]
        age_value.append(roads.loc[:,'teen_pcnt'].values[0])
        age_value.append(roads.loc[:,'twenty_pcnt'].values[0])
        age_value.append(roads.loc[:,'thirty_pcnt'].values[0])
        age_value.append(roads.loc[:,'fourty_pcnt'].values[0])
        age_value.append(roads.loc[:,'fifty_pcnt'].values[0])
        age_value.append(roads.loc[:,'sixty_pcnt'].values[0])
        age_sort = list(age_value)
        age_sort.sort(reverse = True)
        
        awards = 1
        for i in range(6):
            for j in range(6):
                if age_sort[i] == age_value[j]:
                    ret[age_columns[j]] = awards
                    awards += 1
    return ret   

def sales(data, gu, dong):
    areas = data['area'].loc[(data['area']['gu'] == gu) & (data['area']['dong'] == dong),:]['road_name']
    ret = {
        'total' : 0,
        'men' : 0,
        'women' : 0,
        'teen':0,
        'twenty':0,
        'thirty':0,
        'fourty':0,
        'fifty':0,
        'sixty':0,
    }
    roads = data['mean_sales'].loc[data['mean_sales']['road_name'].isin(areas)]
    if roads.size == 0:
        return ret
    # 순서를 메기자 1이 더 높은거!
    else:
        roads = roads.mean()
        ret['total'] = roads.month_sales
        men = roads.men_sales
        women = roads.women_sales
        if men > women :
            ret['men'] = 1
            ret['women'] = 2
        else:
            ret['men'] = 2
            ret['women'] = 1
            
        age_value = []
        age_columns = ["teen","twenty","thirty","fourty","fifty","sixty"]
        age_value.append(roads.teen_sales)
        age_value.append(roads.twenty_sales)
        age_value.append(roads.thirty_sales)
        age_value.append(roads.fourty_sales)
        age_value.append(roads.fifty_sales)
        age_value.append(roads.sixty_sales)
        age_sort = list(age_value)
        age_sort.sort(reverse = True)
        
        awards = 1
        for i in range(6):
            for j in range(6):
                if age_sort[i] == age_value[j]:
                    ret[age_columns[j]] = awards
                    awards += 1
    return ret

def repeatAllRegion(data):
    areas = data['area'].loc[:,['gu', 'dong','dong_code']]
    areas = areas.drop_duplicates()
    areas = areas.groupby(['gu','dong']).max().reset_index()
    matrix = []

    for i,v in areas.iterrows():
    #     break
        region = {
            'gu':v.gu,'dong':v.dong
        }
        #지역 점수, 등급 정보
        point = pointRegion(v.dong_code)
        region['total_score'] = point['total_score']
        region['grothIndex'] = point['grothIndex']
        region['stability'] = point['stability']
        region['salePwr'] = point['salePwr']
        region['buyingPwr'] = point['buyingPwr']
        region['gathPwr'] = point['gathPwr']
        region['grade'] = point['grade']

        #지역 유동인구 순위
        foot = foottraffic(data, v.gu, v.dong)
        if foot['total'] == 0:
            region['foot_men'] = 0
            region['foot_women'] = 0
            region['foot_teen'] = 0
            region['foot_twenty'] = 0
            region['foot_thirty'] = 0
            region['foot_fourty'] = 0
            region['foot_fifty'] = 0
            region['foot_sixty'] = 0
        else:
            region['foot_men'] = foot['men']
            region['foot_women'] = foot['women']
            region['foot_teen'] = foot['teen']
            region['foot_twenty'] = foot['twenty']
            region['foot_thirty'] = foot['thirty']
            region['foot_fourty'] = foot['fourty']
            region['foot_fifty'] = foot['fifty']
            region['foot_sixty'] = foot['sixty']

        #지역 매출액 순위
        sale = sales(data, v.gu, v.dong)
        if sale['total'] == 0:
            region['sale_men'] = 0
            region['sale_women'] = 0
            region['sale_teen'] = 0
            region['sale_twenty'] = 0
            region['sale_thirty'] = 0
            region['sale_fourty'] = 0
            region['sale_fifty'] = 0
            region['sale_sixty'] = 0
        else:
            region['sale_men'] = sale['men']
            region['sale_women'] = sale['women']
            region['sale_teen'] = sale['teen']
            region['sale_twenty'] = sale['twenty']
            region['sale_thirty'] = sale['thirty']
            region['sale_fourty'] = sale['fourty']
            region['sale_fifty'] = sale['fifty']
            region['sale_sixty'] = sale['sixty']

        matrix.append(region)

    return matrix

def import_data(data_path=DATA_FILE):
    """
    Req. 1-1-1 음식점 데이터 파일을 읽어서 Pandas DataFrame 형태로 저장합니다
    """

    try:
        with open(data_path, encoding="utf-8") as f:
            data = json.loads(f.read())
    except FileNotFoundError as e:
        print(f"`{data_path}` 가 존재하지 않습니다.")
        exit(1)

    stores = []  # 음식점 테이블
    reviews = []  # 리뷰 테이블
    menus = [] # 음식점당 메뉴이름 및 가격 정보
    users = []
    now = datetime.datetime.now()
    nowstr = now.strftime('%Y')
    for d in data:

        categories = [c["category"] for c in d["category_list"]]
        stores.append(
            [
                d["id"],
                d["name"],
                d["branch"],
                d["area"],
                d["tel"],
                d["address"],
                d["latitude"],
                d["longitude"],
                "|".join(categories),
                len(d['review_list']),
            ]
        )
        for idx, menu in enumerate(d['menu_list']):
            m = menu['menu']
            p = menu['price']
            menus.append(
                [idx+1,d['id'],m,p]
            )
        for review in d["review_list"]:
            r = review["review_info"]
            u = review["writer_info"]
            users.append(
                [u['id'], u['gender'], int(nowstr)-int(u['born_year'])+1 ]
            )

            reviews.append(
                [r["id"], d["id"], u["id"], r["score"], r["content"], r["reg_time"]]
            )
    # 읽어오고
    df = pd.read_excel('../data/서울 상권정보.xlsx', sheet_name='Sheet1')
    # print(df)
    # print(df.iloc[0:2,:])
    # seoul = df[['상가업소번호','상호명','상권업종중분류명','상권업종소분류명','표준산업분류명','지번주소','경도','위도']]
    store_frame = pd.DataFrame(data=stores, columns=store_columns)
    review_frame = pd.DataFrame(data=reviews, columns=review_columns)
    menu_frame = pd.DataFrame(data=menus, columns=menu_columns)
    user_frame = pd.DataFrame(data=users, columns=user_columns)
    user_frame = user_frame.drop_duplicates()

    ## 기존데이터와 서울상권 합침, 대분류명:'음식' 으로 조건을 안걸고 넣었음.
    # se = df.loc[df["상권업종대분류코드"]=="Q",['상가업소번호','상호명','시군구명','행정동명','상권업종대분류코드','상권업종대분류명',
    # '상권업종중분류코드','상권업종중분류명','상권업종소분류코드','상권업종소분류명','표준산업분류명','지번주소','경도','위도']]
    se = df.loc[(df['시도명']=='서울특별시')&(df['상권업종대분류코드']=='Q'),['상가업소번호','상호명','시군구명','행정동명','행정동코드','상권업종대분류명',
    '상권업종중분류명','상권업종소분류명','표준산업분류명','지번주소','경도','위도','상권업종대분류코드','상권업종중분류코드','상권업종소분류코드', '도로명']]
    st = store_frame[['id','store_name','address','latitude','longitude']]
    
    seoul_store = pd.merge(
        se, st, left_on='지번주소', right_on='address'
    )
    condition = seoul_store['상호명'] == seoul_store['store_name']
    seoul = seoul_store.loc[condition,:]
    # 영어로 할때 추가해야할 부분
    seoul.rename(columns={
        '상가업소번호':'sanga_number',
        '시군구명':'gu',
        '행정동명':'dong',
        '행정동코드':'dong_code',
        '상권업종대분류명':'large_category',
        '상권업종중분류명':'medium_category',
        '상권업종소분류명':'small_category',
        '상권업종대분류코드':'large_code',
        '상권업종중분류코드':'medium_code',
        '상권업종소분류코드':'small_code',
        '표준산업분류명':'pyojun_category',
        '도로명':'road_name'
        },inplace=True)
    #########################
    seoul.road_name = seoul.road_name.str.split().str[2]   ### 데이터 ~~로, ~~길 만 들어가도록 만들었다


    # areas = seoul[['gu','dong','dong_code','road_name']]
    areas = df[['시군구명','행정동명','행정동코드','도로명']]
    areas.rename(columns={
        '시군구명':'gu',
        '행정동명':'dong',
        '행정동코드':'dong_code',
        '도로명':'road_name'
    }, inplace=True)
    areas.road_name=areas.road_name.str.split().str[2]
    areas['dong_code'] = areas.dong_code.astype(str)
    areas['dong_code'] = areas.dong_code.str.slice(start=0, stop=8)
    area_merge = areas.groupby(['gu','dong','dong_code','road_name']).count().reset_index()

    un = seoul['large_category'].unique()
    un_code1 = seoul['large_code'].unique()
    un2 = seoul['medium_category'].unique()
    un_code2 = seoul['medium_code'].unique()
    un3 = seoul['small_category'].unique()
    un_code3 = seoul['small_code'].unique()
    dict1 = {
        'large_category' : pd.Series(un),
        'large_code' : pd.Series(un_code1),
    }
    dict2 = {
        'medium_category' : pd.Series(un2),
        'medium_code' : pd.Series(un_code2),
    }
    dict3 = {
        'small_category' : pd.Series(un3),
        'small_code' : pd.Series(un_code3),
    }
    large = pd.DataFrame(dict1)
    medium = pd.DataFrame(dict2)
    small = pd.DataFrame(dict3)

    # user_rating = review_frame.pivot_table('score', index = "user", columns="store")

    # 유동인구
    df_population = pd.read_csv('../data/유동인구.csv')
    pop = df_population.loc[(df_population["기준_년_코드"]==2019) & (df_population["기준_분기_코드"]==2),:]
    pop.rename(columns={
        '기준_년_코드':'year',
        '기준_분기_코드':'quarter',
        '상권_코드_명':'road',
        '총_유동인구_수':'total_pcnt',
        '남성_유동인구_수':'men_pcnt',
        '여성_유동인구_수':'women_pcnt',
        '연령대_10_유동인구_수':'teen_pcnt',
        '연령대_20_유동인구_수':'twenty_pcnt',
        '연령대_30_유동인구_수':'thirty_pcnt',
        '연령대_40_유동인구_수':'fourty_pcnt',
        '연령대_50_유동인구_수':'fifty_pcnt',
        '연령대_60_이상_유동인구_수':'sixty_pcnt',
        '시간대_1_유동인구_수':'time1_pcnt',
        '시간대_2_유동인구_수':'time2_pcnt',
        '시간대_3_유동인구_수':'time3_pcnt',
        '시간대_4_유동인구_수':'time4_pcnt',
        '시간대_5_유동인구_수':'time5_pcnt',
        '시간대_6_유동인구_수':'time6_pcnt',
        '월요일_유동인구_수':'mon_pcnt',
        '화요일_유동인구_수':'tue_pcnt',
        '수요일_유동인구_수':'wed_pcnt',
        '목요일_유동인구_수':'thr_pcnt',
        '금요일_유동인구_수':'fri_pcnt',
        '토요일_유동인구_수':'sat_pcnt',
        '일요일_유동인구_수':'sun_pcnt'
    },inplace=True)
    pop = pop.drop(columns=['상권_구분_코드', '상권_구분_코드_명', '상권_코드'])
    # pop = pop.drop(columns=['상권_구분_코드', '상권_코드'])

    # 매출액
    df_sales = pd.read_csv('../data/추정매출.csv')
    df_sales.rename(columns={
        '기준_년_코드':'year',
        '기준_분기_코드':'quarter',
        '상권_구분_코드':'code',
        '상권_구분_코드_명':'code_name',
        '상권_코드':'road',
        '상권_코드_명':'road_name',
        '서비스_업종_코드':'medium_category',
        '서비스_업종_코드_명':'medium_name',
        '당월_매출_금액':'month_sales',
        '당월_매출_건수':'month_sales_count',
        '주중_매출_비율':'week_rate',
        '주말_매출_비율':'weekend_rate',
        '월요일_매출_비율':'mon_rate',
        '화요일_매출_비율':'tue_rate',
        '수요일_매출_비율':'wed_rate',
        '목요일_매출_비율':'thr_rate',
        '금요일_매출_비율':'fri_rate',
        '토요일_매출_비율':'sat_rate',
        '일요일_매출_비율':'sun_rate',
        '시간대_00~06_매출_비율':'time1_rate',
        '시간대_06~11_매출_비율':'time2_rate',
        '시간대_11~14_매출_비율':'time3_rate',
        '시간대_14~17_매출_비율':'time4_rate',
        '시간대_17~21_매출_비율':'time5_rate',
        '시간대_21~24_매출_비율':'time6_rate',
        '남성_매출_비율':'men_rate',
        '여성_매출_비율':'women_rate',
        '연령대_10_매출_비율':'teen_rate',
        '연령대_20_매출_비율':'twenty_rate',
        '연령대_30_매출_비율':'thirty_rate',
        '연령대_40_매출_비율':'fourty_rate',
        '연령대_50_매출_비율':'fifty_rate',
        '연령대_60_이상_매출_비율':'sixty_rate',
        '주중_매출_금액':'week_sales',
        '주말_매출_금액':'weekend_sales',
        '월요일_매출_금액':'mon_sales',
        '화요일_매출_금액':'tue_sales',
        '수요일_매출_금액':'wed_sales',
        '목요일_매출_금액':'thr_sales',
        '금요일_매출_금액':'fri_sales',
        '토요일_매출_금액':'sat_sales',
        '일요일_매출_금액':'sun_sales',
        '시간대_00~06_매출_금액':'time1_sales',
        '시간대_06~11_매출_금액':'time2_sales',
        '시간대_11~14_매출_금액':'time3_sales',
        '시간대_14~17_매출_금액':'time4_sales',
        '시간대_17~21_매출_금액':'time5_sales',
        '시간대_21~24_매출_금액':'time6_sales',
        '남성_매출_금액':'men_sales',
        '여성_매출_금액':'women_sales',
        '연령대_10_매출_금액':'teen_sales',
        '연령대_20_매출_금액':'twenty_sales',
        '연령대_30_매출_금액':'thirty_sales',
        '연령대_40_매출_금액':'fourty_sales',
        '연령대_50_매출_금액':'fifty_sales',
        '연령대_60_이상_매출_금액':'sixty_sales',
        '점포수':'store_cnt'
    },inplace=True)
    sales_group = df_sales.loc[df_sales['code'] == "A", :].groupby(["road","road_name"])

    mean_rate = sales_group.mean().loc[:,[
        'week_rate','weekend_rate',
        'mon_rate','tue_rate','wed_rate','thr_rate','fri_rate','sat_rate','sun_rate',
        'men_rate','women_rate',
        'time1_rate','time2_rate','time3_rate','time4_rate','time5_rate','time6_rate',
        'teen_rate','twenty_rate','thirty_rate','fourty_rate','fifty_rate','sixty_rate'
    ]].reset_index()

    sum_sales = sales_group.sum().loc[:,[
        'month_sales','week_sales','weekend_sales',
        'mon_sales','tue_sales','wed_sales','thr_sales','fri_sales','sat_sales','sun_sales',
        'time1_sales','time2_sales','time3_sales','time4_sales','time5_sales','time6_sales',
        'men_sales','women_sales',
        'teen_sales','twenty_sales','thirty_sales','fourty_sales','fifty_sales','sixty_sales',
        'store_cnt'
    ]]    
    # 모든 길의 지점당 월평균 매출액
    # 만약 지점당 하지 않고 전체 지역으로 한다면 이 과정은 거치지 않아도 된다!
    mean_sales = sum_sales.apply(lambda x: (x / 10000) / sum_sales['store_cnt'],axis=0).reset_index()


    dev_sales_group = df_sales.loc[df_sales['code'] == "D", :].groupby(["road","road_name"])

    dev_mean_rate = dev_sales_group.mean().loc[:,[
        'week_rate','weekend_rate',
        'mon_rate','tue_rate','wed_rate','thr_rate','fri_rate','sat_rate','sun_rate',
        'men_rate','women_rate',
        'time1_rate','time2_rate','time3_rate','time4_rate','time5_rate','time6_rate',
        'teen_rate','twenty_rate','thirty_rate','fourty_rate','fifty_rate','sixty_rate'
    ]].reset_index()

    dev_sum_sales = dev_sales_group.sum().loc[:,[
        'month_sales','week_sales','weekend_sales',
        'mon_sales','tue_sales','wed_sales','thr_sales','fri_sales','sat_sales','sun_sales',
        'time1_sales','time2_sales','time3_sales','time4_sales','time5_sales','time6_sales',
        'men_sales','women_sales',
        'teen_sales','twenty_sales','thirty_sales','fourty_sales','fifty_sales','sixty_sales',
        'store_cnt'
    ]]    
    # 모든 길의 지점당 월평균 매출액
    # 만약 지점당 하지 않고 전체 지역으로 한다면 이 과정은 거치지 않아도 된다!
    dev_mean_sales = dev_sum_sales.apply(lambda x: (x / 10000) / dev_sum_sales['store_cnt'],axis=0).reset_index()

    dev_mean_rate['road_name'] = dev_mean_rate['road_name'].str.split().str[2].fillna('0')
    dev_mean_rate = dev_mean_rate.loc[dev_mean_rate['road_name']!='0',:]
    dev_mean_rate['road_name'] = dev_mean_rate['road_name'].str.split('_').str[0]
    dev_mean_rate=dev_mean_rate.loc[dev_mean_rate['road_name'].str.endswith('역'),:]
    
    
    dev_mean_sales['road_name'] = dev_mean_sales['road_name'].str.split().str[2].fillna('0')
    dev_mean_sales = dev_mean_sales.loc[dev_mean_sales['road_name']!='0',:]
    dev_mean_sales['road_name'] = dev_mean_sales['road_name'].str.split('_').str[0]
    dev_mean_sales=dev_mean_sales.loc[dev_mean_sales['road_name'].str.endswith('역'),:]

    
    df = {
        "stores": seoul, "reviews": review_frame, 'menus': menu_frame, 'users':user_frame,'area':area_merge,
        'large':large,'medium':medium,'small':small,'population':pop, 'mean_rate':mean_rate, 
        'mean_sales':mean_sales, 'dev_mean_rate':dev_mean_rate, 'dev_mean_sales':dev_mean_sales
        }

    #전체 지역의 특성을 정제하자.
    matrix = repeatAllRegion(df)

    # 그 결과를 기준으로 유사도를 계산하자.
    df_kmeans = pd.DataFrame(matrix)
    df_kmeans = df_kmeans.groupby(['gu','dong']).sum()

    from sklearn.cluster import KMeans
    X = df_kmeans.values
    model = KMeans(n_clusters=20,init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
    model.fit(X)
    predict = pd.DataFrame(model.predict(X))
    predict.columns=['predict']
    df_kmeans = df_kmeans.reset_index()
    df_kmeans['predict'] = predict
    df_kmeans = df_kmeans.loc[:,['gu','dong','predict']]
    df['similarity'] = df_kmeans
    df['recommend'] = pd.DataFrame(allRecommend(df))

    return df



def dump_dataframes(dataframes):
    
    pd.to_pickle(dataframes, DUMP_FILE)


def load_dataframes():
    return pd.read_pickle(DUMP_FILE)


def main():

    print("[*] Parsing data...")
    data = import_data()
    print("[+] Done")

    print("[*] Dumping data...")
    dump_dataframes(data)
    print("[+] Done\n")

    data = load_dataframes()

    term_w = shutil.get_terminal_size()[0] - 1
    separater = "-" * term_w

    # print("[음식점]")
    # print(f"{separater}\n")
    # print(data["stores"].head())
    # print(f"\n{separater}\n\n")

    # print("[메뉴]")
    # print(f"{separater}\n")
    # print(data["menus"].head())
    # print(f"\n{separater}\n\n")

    # print("[리뷰]")
    # print(f"{separater}\n")
    # print(data["reviews"].head())
    # print(f"\n{separater}\n\n")
    
    # print("[User]")
    # print(f"{separater}\n")
    # print(data["users"].head())
    # print(f"\n{separater}\n\n")
    # print("[User]")

    # print(f"{separater}\n")
    # print(data["seoul"].head())
    # print(f"\n{separater}\n\n")


if __name__ == "__main__":
    main()
