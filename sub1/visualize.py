import itertools
from collections import Counter
from parse import load_dataframes
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import folium
from folium.plugins import MarkerCluster

def set_config():
    # 폰트, 그래프 색상 설정
    font_list = fm.findSystemFonts(fontpaths=None, fontext="ttf")
    if any(["notosanscjk" in font.lower() for font in font_list]):
        plt.rcParams["font.family"] = "Noto Sans CJK JP"
    else:
        if not any(["malgun" in font.lower() for font in font_list]):
            raise Exception(
                "Font missing, please install Noto Sans CJK or Malgun Gothic. If you're using ubuntu, try `sudo apt install fonts-noto-cjk`"
            )

        plt.rcParams["font.family"] = "Malgun Gothic"

    sns.set_palette(sns.color_palette("Spectral"))
    plt.rc("xtick", labelsize=6)


def show_store_categories_graph(dataframes, n=100):
    """
    Tutorial: 전체 음식점의 상위 `n`개 카테고리 분포를 그래프로 나타냅니다.
    """

    stores = dataframes["stores"]

    # 모든 카테고리를 1차원 리스트에 저장합니다
    categories = stores.category.apply(lambda c: c.split("|"))
    categories = itertools.chain.from_iterable(categories)

    # 카테고리가 없는 경우 / 상위 카테고리를 추출합니다
    categories = filter(lambda c: c != "", categories)
    categories_count = Counter(list(categories))
    best_categories = categories_count.most_common(n=n)
    df = pd.DataFrame(best_categories, columns=["category", "count"]).sort_values(
        by=["count"], ascending=False
    )
    print(len(categories_count))
    # 그래프로 나타냅니다
    chart = sns.barplot(x="category", y="count", data=df)
    chart.set_xticklabels(chart.get_xticklabels(), rotation=45)
    plt.title("음식점 카테고리 분포")
    plt.show() 


def show_store_review_distribution_graph(dataframes):
    """
    Req. 1-3-1 전체 음식점의 리뷰 개수 분포를 그래프로 나타냅니다. 
    """
    cnt = dataframes['stores'][['store_name','review_count']]
    # 리뷰가 1개인 음식점의 수가 매우 많아서 전체적인 분포를 확인하기 어렵다. 구간을 나눠서 각각의 표를 보기로함

    condition1 = (cnt['review_count']>=0)&(cnt['review_count']<=2)
    condition2 = (cnt['review_count']>2)&(cnt['review_count']<=7)
    condition3 = (cnt['review_count']>7)&(cnt['review_count']<=20)
    condition4 = (cnt['review_count']>20)
    cnt1 = cnt.loc[condition1,:]
    cnt2 = cnt.loc[condition2,:]
    cnt3 = cnt.loc[condition3,:]
    cnt4 = cnt.loc[condition4,:]
    fig = plt.figure()
    ax1 = fig.add_subplot(2,2,1)
    ax2 = fig.add_subplot(2,2,2)
    ax3 = fig.add_subplot(2,2,3)
    ax4 = fig.add_subplot(2,2,4)
    
    plt.title('음식점 리뷰개수')
    ax1.hist(cnt1['review_count'], bins=5)
    ax2.hist(cnt2['review_count'], bins=10)
    ax3.hist(cnt3['review_count'], bins=15)
    ax4.hist(cnt4['review_count'], bins=50)
    plt.show()


def show_store_average_ratings_graph(dataframes):
    """
    Req. 1-3-2 각 음식점의 평균 평점을 그래프로 나타냅니다.
    """

    stores_reviews = pd.merge(
        dataframes['stores'], dataframes['reviews'], left_on='id', right_on='store'
    )
    store_group  = stores_reviews.groupby(['store','store_name'])
    score = store_group.mean()
    score = score.reset_index()
    ## 평점의 경우 0~5점까지 범위가 정해져 있기때문에 boxplot을 사용하여 음식점들의 평점이 어느 분포로 받는지 알 수있다. 
    score.plot(kind='box',y='score')
    plt.title('음식점 평균 평점 분포')
    plt.show()

def show_user_review_distribution_graph(dataframes):
    """
    Req. 1-3-3 전체 유저의 리뷰 개수 분포를 그래프로 나타냅니다.
    """
    users_reviews = pd.merge(
        dataframes['users'], dataframes['reviews'], left_on='id', right_on='user'
    )
    user_group = users_reviews.groupby(['user'])
    cnt = user_group.count()
    ## 리뷰의 개수에서 outlier로 인해 원하는 데이터 시각화가 안나오기때문에 범위를 조정해서 시각화 했다. 
    condition1 = (cnt['id_x']>5)&(cnt['id_x']<700)
    cnt = cnt.loc[condition1,:]
    cnt = cnt.reset_index()
    cnt.plot(kind='hist',y='id_x',bins=150)
    # chart = sns.barplot(x='user', y='id_x', data=cnt)
    # chart.set_xticklabels(chart.get_xticklabels(), rotation=45)
    plt.title('유저의 리뷰개수')
    plt.show()


def show_user_age_gender_distribution_graph(dataframes):
    """
    Req. 1-3-4 전체 유저의 성별/나이대 분포를 그래프로 나타냅니다.
    """
    users = dataframes['users']
    # users = users.loc[condition,'']
    male = users[users['gender']=='남']
    female = users[users['gender']=='여']

    plt.hist(female['age'],bins=200, alpha=0.5, color='green',label='female')
    plt.hist(male['age'],bins=200, alpha=0.6,color='blue', label='male')

    # sns.distplot(male['age'],color='blue', label='남',hist=False, bins=10)
    # sns.distplot(female['age'],color='red', label='여', hist=False, bins=10)
    # plt.axis([0, 100, 0, 0.03])
    plt.xlim(0,100)
    plt.xlabel('나이')
    plt.ylabel('회원수')
    plt.show()

def show_stores_distribution_graph(dataframes):
    """
    Req. 1-3-5 각 음식점의 위치 분포를 지도에 나타냅니다.
    """

    stores = dataframes['stores']
    # condition : 지역(area) + review_count가 1이상?
    condition = (stores['area'] == '제주')&(stores['review_count']>0)
    df = stores[condition]
    print(df)

    map_test = folium.Map(location=[36.5053542,127.7043419], zoom_start=8)
    marker_cluster = MarkerCluster().add_to(map_test)

    for idx in range(len(df)):
        lat = df.iloc[idx,6]
        lon = df.iloc[idx,7]
        if not lat or not lon: continue
        location = (float(lat), float(lon))
        folium.Marker(location,popup=df.iloc[idx,1]).add_to(marker_cluster)
    map_test.save('map1.html')
    


def main():
    set_config()
    data = load_dataframes()

    show_store_categories_graph(data)
    
    # show_store_review_distribution_graph(data)

    # show_store_average_ratings_graph(data)
    
    # show_user_review_distribution_graph(data)

    # show_user_age_gender_distribution_graph(data)

    # show_stores_distribution_graph(data)


if __name__ == "__main__":
    main()
