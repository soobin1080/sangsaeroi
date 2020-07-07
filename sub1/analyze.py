from parse import load_dataframes
import pandas as pd
import shutil
import numpy as np


def sort_stores_by_score(dataframes, n=20, min_reviews=4):
    """
    Req. 1-2-1 각 음식점의 평균 평점을 계산하여 높은 평점의 음식점 순으로 `n`개의 음식점을 정렬하여 리턴합니다
    Req. 1-2-2 리뷰 개수가 `min_reviews` 미만인 음식점은 제외합니다.
    """
    stores_reviews = pd.merge(
        dataframes["seoul_stores"], dataframes["reviews"], left_on="id", right_on="store"
    )
    scores_group = stores_reviews.groupby(["store", "store_name"])
    scores = scores_group.mean()
    cnt = scores_group.count()
    # scores = scores.loc[scores['review_count']>=min_reviews,:]
    scores = scores.loc[cnt['id_x']>min_reviews,:]
    scores.sort_values(by='score',ascending=False,inplace=True)
    return scores.head(n=n).reset_index()


def get_most_reviewed_stores(dataframes, n=30):
    """
    Req. 1-2-3 가장 많은 리뷰를 받은 `n`개의 음식점을 정렬하여 리턴합니다
    """
    sotores_reivews = pd.merge(
        dataframes['seoul_stores'], dataframes['reviews'], left_on='id', right_on='store'
    )
    reviews_group = sotores_reivews.groupby(['store','store_name'])
    counts = reviews_group.count()
    # print(counts.loc[counts['id_x']>=0,:].shape)
    print(dataframes['seoul_stores'].info())
    print(counts)
    counts.sort_values(by='id_x', ascending=False, inplace=True)
    return counts.head(n=n).reset_index()


def get_most_active_users(dataframes, n=20):
    """
    Req. 1-2-4 가장 많은 리뷰를 작성한 `n`명의 유저를 정렬하여 리턴합니다.
    """
    users_review = pd.merge(
        dataframes['users'], dataframes['reviews'],left_on='id', right_on='user'
    )
    user_group = users_review.groupby(['user'])
    counts = user_group.count()
    counts.sort_values(by='age',ascending=False, inplace=True)
    return counts.head(n=n).reset_index()


def get_user_review(dataframes, n=20):
    users_reviews = pd.merge(
        dataframes['users'], dataframes['reviews'], left_on='id', right_on='user'
    )
    user_group = users_reviews.groupby(['user'])
    print(user_group.head())
    
    return

def get_merge_store_seoul(dataframes, n=20):
    m = dataframes['dev_mean_sales']
    n = dataframes['dev_mean_rate']
    # print(m.iloc[:,:8])

    print(m.info())
    print(m)
    print('#####33')
    print(n.info())
    print(n)
    # m['road_name'] = m['road_name'].str.split().str[2].fillna(0)
    # print(m['road_name'])
    # m_station = m.loc[m['road_name']!=0,:]
    # print(m_station)
    # m_station['road_name'] = m_station['road_name'].str.split('_').str[0]
    # print(m_station['road_name'])
    # print(m_station.loc[m_station['road_name'].str.endswith('역'),:])
def mf(dataframes):

    # 리뷰상점 리스트
    stores = dataframes['stores']
    stores.rename(columns={'id':'store'}, inplace = True)
    ratings_stores = pd.merge(dataframes['reviews'], stores, on='store')

    # 사용자 유사도 결과
    user_sim_df = extractUserSimilarity(dataframes)

    # 해당 지역에 있는 리뷰데이터를 Merge해서 어떤 사용자가 이 지역에서 음식을 먹었는지 보자 "신사동" 대신에 입력받은 주소 넣으면 됨
    pick = dataframes['stores'].loc[dataframes['stores']['dong'] == "충현동",:]
    pick.rename(columns={'id':'store'}, inplace = True)
    merge_picked = pd.merge(pick, dataframes['reviews'], on='store')
    picked_users = merge_picked.groupby(["user"])["user"]
    print(picked_users.head())

    # 어떤 유저들이 있니?
    user_list = list()
    for userid, index in picked_users:
        user_list.append(userid)

  # 위 유저들과 유사한 유저들은 어떻게 되어있니?
    over_sim = list()
    for i in user_list:
        top_sim = user_sim_df[i].sort_values(ascending=False)[0:10]
        for j in top_sim.index:
            if(top_sim[j] > 0.7):
                over_sim.append(j)
    # len(over_sim)
    print(over_sim)
    

    # 뽑아낸 유저들의 선호 카테고리는? 
    over_sim = pd.DataFrame(over_sim)
    over_sim["user"] = pd.DataFrame(over_sim)
    over_sim_merge = pd.merge(over_sim, ratings_stores, on="user")
    # print(over_sim_merge.columns)
    over_sim_merge = over_sim_merge.groupby(["small_category"]).mean()
    # over_sim_merge = over_sim_merge.groupby(["small_category_id","small_category_name"]).mean()
    over_sim_merge = over_sim_merge.sort_values(by="score", ascending=False)
    print(over_sim_merge["score"])
    
    # 선택한 지역의 카테고리 점수 뽑기 (여기서는 아직 리뷰 개수로 제한 두진 않았다)
    picked_medium_category = merge_picked.groupby(["small_category"]).mean()
    picked_medium_category = picked_medium_category.sort_values(by="score", ascending=False)
    print(picked_medium_category["score"])



    top_avg_category = extractDongPopulation(dataframes, "충현동")
    print(top_avg_category)

    answer = pd.merge(top_avg_category, dataframes["small"], on="small_code")[["small_code","small_category", "score"]]
    print(answer.head(10))


def extractUserSimilarity(dataframes):
    # 서울 음식점 데이터만 사용
    stores = dataframes['stores']
    stores.rename(columns={'id':'store'}, inplace = True)

    # 서울 음식점 중 리뷰가 있는 음식점만 
    ratings_stores = pd.merge(dataframes['reviews'], stores, on='store')

    # 한 사람이 하나의 음식점에 여러개 리뷰를 달 수 있으니 해당 음식점과 유저로 그룹바이 한 뒤 평점
    group = ratings_stores.groupby(["store", "store_name", "user"])
    mean = group.mean().reset_index()

    user_rating_store = mean.pivot_table('score', index='user', columns="store_name").fillna(0)

    # 유저 유사도
    from sklearn.metrics.pairwise import cosine_similarity
    user_sim = cosine_similarity(user_rating_store, user_rating_store)
    user_sim_df = pd.DataFrame(data = user_sim, index = user_rating_store.index, columns = user_rating_store.index)

    return user_sim_df

def extractDongPopulation(dataframes, dong):
    # 입력받는 행정동에 포함되는 도로명 주소들을 뽑아낸다.
    dong_stores = dataframes['stores'].loc[dataframes['stores']['dong'] == dong ,['road_name']]
    dong_stores = dong_stores.groupby(['road_name'])
    ro = []
    for item, i in dong_stores:
        ro.append(item.split()[2])

    # 입력받는 행정동에 있는 도로명주소의 유동인구들 합을 뽑아보자!
    pop = dataframes['population']
    road_popul = pop.loc[(pop["road"].isin(ro))].groupby(["year"])
    road_popul = road_popul.sum().reset_index()
    road_popul

    # 성별
    gender = road_popul.loc[:,['men_pcnt','women_pcnt']]
    gender_values = []
    for i in gender:
        str = i
        str += " " + np.array2string(gender[i].values[0])
        str += "명"
        gender_values.append(str)
    
    # 나이대
    ages = road_popul.loc[:,['teen_pcnt','twenty_pcnt','thirty_pcnt','fourty_pcnt','fifty_pcnt','sixty_pcnt']]
    ages_columns = ["10대","20대","30대","40대","50대","60대 이상",]
    ages_values = []
    index = 0
    for i in ages:
        str = ages_columns[index]
        index += 1
        str += " " + np.array2string(ages[i].values[0])
        str += "명"
        ages_values.append(str)
        
    # 시간대
    times = road_popul.loc[:,['time1_pcnt','time2_pcnt','time3_pcnt','time4_pcnt','time5_pcnt','time6_pcnt']]
    times_columns = ["00시~06시", "06시~11시", "11시~14시", "14시~17시", "17시~21시", "21시~24시"]
    times_values = []
    index = 0
    for i in times:
        str = times_columns[index]
        index += 1
        str += " " + np.array2string(times[i].values[0])
        str += "명"
        times_values.append(str)

    # 요일별
    days = road_popul.loc[:,['mon_pcnt','tue_pcnt','wed_pcnt','thr_pcnt','fri_pcnt','sat_pcnt','sun_pcnt']]
    days_columns=["월","화","수","목","금","토","일"]
    days_values = []
    index = 0
    for i in days:
        str = days_columns[index]
        index += 1
        str += " " + np.array2string(days[i].values[0])
        str += "명"
        days_values.append(str)
    
    # 어떤 나이대가 가장 많은가
    ages = road_popul.loc[:,['teen_pcnt','twenty_pcnt','thirty_pcnt','fourty_pcnt','fifty_pcnt','sixty_pcnt']]
    ages_columns = ["10대","20대","30대","40대","50대","60대 이상",]
    ages_values = []
    index = 0
    max_ages = ages['teen_pcnt'].values[0]
    max_ages_id = 0
    for i in ages:
        if max_ages < ages[i].values[0]:
            max_ages = ages[i].values[0]
            max_ages_id = index
        str = ages_columns[index]
        index += 1
        str += " " + np.array2string(ages[i].values[0])
        str += "명"
        ages_values.append(str)

    # 그럼 가장 많은 나이대의 유저들만 뽑아서 어떤 카테고리에 리뷰를 가장 많이 남겼으며, 어떤 카테고리에 평점을 가장 좋게 줬는데 볼까?
    if max_ages_id == 0:
        min_scope = 10
        max_scope = 19
    elif max_ages_id == 1:
        min_scope = 20
        max_scope = 29
    elif max_ages_id == 2:
        min_scope = 30
        max_scope = 39
    elif max_ages_id == 3:
        min_scope = 40
        max_scope = 49
    elif max_ages_id == 4:
        min_scope = 50
        max_scope = 59
    elif max_ages_id == 5:
        min_scope = 60
        max_scope = 99

    users = dataframes['users']
    users.rename(columns={'id':'user'},inplace=True)

    stores = dataframes['stores']
    stores.rename(columns={'id':'store'}, inplace = True)
    # 서울 음식점 중 리뷰가 있는 음식점만 
    ratings_stores = pd.merge(dataframes['reviews'], stores, on='store')
    ratings_stores.columns
    user_store_review_merge = pd.merge(users, ratings_stores, on='user')
    user_store_review_merge = user_store_review_merge.loc[(user_store_review_merge["age"] >= min_scope) & (user_store_review_merge["age"] <= max_scope),:]

    # 가장 많은 나이대의 사람들이 가장 리뷰를 많이 남긴 순 음식점 카테고리
    count_category = user_store_review_merge.groupby(["small_code"])
    count_category = count_category.count().sort_values(by="small_code")
    top_count_category = count_category.sort_values(by="id", ascending = False)[0:10]

    # 가장 많은 나이대의 사람들이 평균이 높은 순 음식점 카테고리
    avg_category = user_store_review_merge.groupby(["small_code"]).mean().sort_values(by="small_code")
    avg_category["count"] = count_category["score"]
    avg_category = avg_category.loc[avg_category["count"] > 200, :][["score", "count"]]
    top_avg_category = avg_category.sort_values(by="score", ascending=False)[0:10]
    # print(top_avg_category)

    return top_avg_category


def main():
    data = load_dataframes()

    term_w = shutil.get_terminal_size()[0] - 1
    separater = "-" * term_w

    # stores_most_scored = sort_stores_by_score(data)
    # most_reviewed_stores = get_most_reviewed_stores(data)
    # most_active_users = get_most_active_users(data)

    # get_user_review(data)
    get_merge_store_seoul(data)
    # mf(data)
    # print("[최고 평점 음식점]")
    # print(f"{separater}\n")
    # for i, store in stores_most_scored.iterrows():
    #     print(
    #         "{rank}위: {store}({score:2f}점)".format(
    #             rank=i + 1, store=store.store_name, score=store.score
    #         )
    #     )
    # print(f"\n{separater}\n\n")

    # print("[리뷰가 가장많은 음식점]")
    # print(f"{separater}\n")
    # for i, store in most_reviewed_stores.iterrows():
    #     print(
    #         "{rank}위: 상호명 : {store} 리뷰수 : {score}개".format(
    #             rank=i + 1, store=store.store_name, score=store.score
    #         )
    #     )
    # print(f"\n{separater}\n\n")

    # print("[리뷰가 가장많은 사용자]")
    # print(f"{separater}\n")
    # for i, user in most_active_users.iterrows():
    #     print(
    #         "{rank}위:  ID : {user}, 리뷰수 : {cnt}개".format(
    #             rank=i + 1, user=user.user, cnt=user.age
    #         )
    #     )
    # print(f"\n{separater}\n\n")

    
if __name__ == "__main__":
    main()
