from pathlib import Path
import pandas as pd
from django.core.management.base import BaseCommand
from backend import settings
from api import models


class Command(BaseCommand):
    help = "initialize database"
    DATA_DIR = Path(settings.BASE_DIR).parent.parent / "data"
    DATA_FILE = str(DATA_DIR / "dump.pkl")

    def _load_dataframes(self):
        try:
            data = pd.read_pickle(Command.DATA_FILE)
        except:
            print(f"[-] Reading {Command.DATA_FILE} failed")
            exit(1)
        return data

    def _initialize(self):
        """
        Sub PJT 1에서 만든 Dataframe을 이용하여 DB를 초기화합니다.
        """
        print("[*] Loading data...")
        dataframes = self._load_dataframes()

        print("[*] Initializing stores...")
        models.Area.objects.all().delete()
        models.LargeCategory.objects.all().delete()
        models.MediumCategory.objects.all().delete()
        models.SmallCategory.objects.all().delete()
        models.FootTraffic.objects.all().delete()
        models.MeanSale.objects.all().delete()
        models.MeanSaleRate.objects.all().delete()
        models.DevMeanSale.objects.all().delete()
        models.DevMeanSaleRate.objects.all().delete()
        models.recommendResult.objects.all().delete()
        print('[#] modeling start')
        area = dataframes['area']
        area_bulk = []
        cnt = 1
        for ar in area.itertuples():
            area_bulk.append(
                models.Area(
                    id=cnt,
                    gu=ar.gu,
                    dong=ar.dong,
                    dong_code=ar.dong_code,
                    road_name=ar.road_name
                )
            )
            cnt += 1
        models.Area.objects.bulk_create(area_bulk)   

        large = dataframes['large']
        large_bulk = []
        for la in large.itertuples():
            large_bulk.append(
                models.LargeCategory(
                    code=la.large_code,
                    name=la.large_category
                )
            )
        models.LargeCategory.objects.bulk_create(large_bulk)

        medium = dataframes['medium']
        medium_bulk = []
        for me in medium.itertuples():
            medium_bulk.append(
                models.MediumCategory(
                    code=me.medium_code,
                    name=me.medium_category
                )
            )
        models.MediumCategory.objects.bulk_create(medium_bulk)

        small = dataframes['small']
        small_bulk = []
        for sm in small.itertuples():
            small_bulk.append(
                models.SmallCategory(
                    code=sm.small_code,
                    name=sm.small_category
                )
            )
        models.SmallCategory.objects.bulk_create(small_bulk)

        print('[$$] FootTraffic')
        foots = dataframes['population']
        foots_bulk = []
        cnt = 0
        for foot in foots.itertuples():
            if not models.Area.objects.filter(road_name=foot.road).exists(): continue
            cnt += 1
            foots_bulk.append(
                models.FootTraffic(
                    id=cnt,
                    road = models.Area.objects.filter(road_name=foot.road)[0],
                    total_pcnt = foot.total_pcnt,
                    men_pcnt = foot.men_pcnt,
                    women_pcnt = foot.women_pcnt,
                    teen_pcnt = foot.teen_pcnt,
                    twenty_pcnt = foot.twenty_pcnt,
                    thirty_pcnt = foot.thirty_pcnt,
                    fourty_pcnt = foot.fourty_pcnt,
                    fifty_pcnt = foot.fifty_pcnt,
                    sixty_pcnt = foot.sixty_pcnt,
                    time1_pcnt = foot.time1_pcnt,
                    time2_pcnt = foot.time2_pcnt,
                    time3_pcnt = foot.time3_pcnt,
                    time4_pcnt = foot.time4_pcnt,
                    time5_pcnt = foot.time5_pcnt,
                    time6_pcnt = foot.time6_pcnt,

                    mon_pcnt = foot.mon_pcnt,
                    tue_pcnt = foot.tue_pcnt,
                    wed_pcnt = foot.wed_pcnt,
                    thr_pcnt = foot.thr_pcnt,
                    fri_pcnt = foot.fri_pcnt,
                    sat_pcnt = foot.sat_pcnt,
                    sun_pcnt = foot.sun_pcnt
                )
            )
        models.FootTraffic.objects.bulk_create(foots_bulk)

        print('[@@] MeanSale')
        meansales = dataframes['mean_sales']
        meansale_bulk = []
        cnt = 0
        for ms in meansales.itertuples():
            if not models.Area.objects.filter(road_name=ms.road_name).exists(): continue
            cnt += 1
            meansale_bulk.append(
                models.MeanSale(
                    id=cnt,
                    area=models.Area.objects.filter(road_name=ms.road_name)[0],
                    month = ms.month_sales,
                    week = ms.week_sales,
                    weekend = ms.weekend_sales,
                    mon = ms.mon_sales,
                    tue = ms.tue_sales,
                    wed = ms.wed_sales,
                    thr = ms.thr_sales,
                    fri = ms.fri_sales,
                    sat = ms.sat_sales,
                    sun = ms.sun_sales,
                    time1 = ms.time1_sales,
                    time2 = ms.time2_sales,
                    time3 = ms.time3_sales,
                    time4 = ms.time4_sales,
                    time5 = ms.time5_sales,
                    time6 = ms.time6_sales,
                    men = ms.men_sales,
                    women = ms.women_sales,
                    teen = ms.teen_sales,
                    twenty = ms.twenty_sales,
                    thirty = ms.thirty_sales,
                    fourty = ms.fourty_sales,
                    fifty = ms.fifty_sales,
                    sixty = ms.sixty_sales,
                )
            )
        models.MeanSale.objects.bulk_create(meansale_bulk)

        print('[***] MeanSaleRate')
        rates = dataframes['mean_rate']
        rate_bulk = []
        cnt = 0
        for ms in rates.itertuples():
            if not models.Area.objects.filter(road_name=ms.road_name).exists(): continue            
            cnt += 1

            rate_bulk.append(
                models.MeanSaleRate(
                    id=cnt,
                    area=models.Area.objects.filter(road_name=ms.road_name)[0],
                    week = ms.week_rate,
                    weekend = ms.weekend_rate,
                    mon = ms.mon_rate,
                    tue = ms.tue_rate,
                    wed = ms.wed_rate,
                    thr = ms.thr_rate,
                    fri = ms.fri_rate,
                    sat = ms.sat_rate,
                    sun = ms.sun_rate,
                    time1 = ms.time1_rate,
                    time2 = ms.time2_rate,
                    time3 = ms.time3_rate,
                    time4 = ms.time4_rate,
                    time5 = ms.time5_rate,
                    time6 = ms.time6_rate,
                    men = ms.men_rate,
                    women = ms.women_rate,
                    teen = ms.teen_rate,
                    twenty = ms.twenty_rate,
                    thirty = ms.thirty_rate,
                    fourty = ms.fourty_rate,
                    fifty = ms.fifty_rate,
                    sixty = ms.sixty_rate,
                )
            )
        models.MeanSaleRate.objects.bulk_create(rate_bulk)

        print('[@@] DevMeanSale')
        meansales = dataframes['dev_mean_sales']
        meansale_bulk = []
        cnt = 0
        for ms in meansales.itertuples():
            cnt += 1
            meansale_bulk.append(
                models.DevMeanSale(
                    id=cnt,
                    area=ms.road_name,
                    month = ms.month_sales,
                    week = ms.week_sales,
                    weekend = ms.weekend_sales,
                    mon = ms.mon_sales,
                    tue = ms.tue_sales,
                    wed = ms.wed_sales,
                    thr = ms.thr_sales,
                    fri = ms.fri_sales,
                    sat = ms.sat_sales,
                    sun = ms.sun_sales,
                    time1 = ms.time1_sales,
                    time2 = ms.time2_sales,
                    time3 = ms.time3_sales,
                    time4 = ms.time4_sales,
                    time5 = ms.time5_sales,
                    time6 = ms.time6_sales,
                    men = ms.men_sales,
                    women = ms.women_sales,
                    teen = ms.teen_sales,
                    twenty = ms.twenty_sales,
                    thirty = ms.thirty_sales,
                    fourty = ms.fourty_sales,
                    fifty = ms.fifty_sales,
                    sixty = ms.sixty_sales,
                )
            )
        models.DevMeanSale.objects.bulk_create(meansale_bulk)

        print('[***] DevMeanSaleRate')
        rates = dataframes['dev_mean_rate']
        rate_bulk = []
        cnt = 0
        for ms in rates.itertuples():
            cnt += 1

            rate_bulk.append(
                models.DevMeanSaleRate(
                    id=cnt,
                    area=ms.road_name,
                    week = ms.week_rate,
                    weekend = ms.weekend_rate,
                    mon = ms.mon_rate,
                    tue = ms.tue_rate,
                    wed = ms.wed_rate,
                    thr = ms.thr_rate,
                    fri = ms.fri_rate,
                    sat = ms.sat_rate,
                    sun = ms.sun_rate,
                    time1 = ms.time1_rate,
                    time2 = ms.time2_rate,
                    time3 = ms.time3_rate,
                    time4 = ms.time4_rate,
                    time5 = ms.time5_rate,
                    time6 = ms.time6_rate,
                    men = ms.men_rate,
                    women = ms.women_rate,
                    teen = ms.teen_rate,
                    twenty = ms.twenty_rate,
                    thirty = ms.thirty_rate,
                    fourty = ms.fourty_rate,
                    fifty = ms.fifty_rate,
                    sixty = ms.sixty_rate,
                )
            )
        models.DevMeanSaleRate.objects.bulk_create(rate_bulk)
        
        print("[***] recommend Result")
        recommend = dataframes['recommend']
        recommend_bulk = []
        cnt = 0

        for rec in recommend.itertuples():
            cnt += 1

            recommend_bulk.append(
                models.recommendResult(
                    id=cnt,
                    gu=rec.gu,
                    dong=rec.dong,
                    result=rec.result
                )
            )
        models.recommendResult.objects.bulk_create(recommend_bulk)


        print("[+] Done")

    def handle(self, *args, **kwargs):
        self._initialize()
