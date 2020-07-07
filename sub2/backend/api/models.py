from django.utils import timezone
from django.db import models
from django.conf import settings


class LargeCategory(models.Model):
    code = models.CharField(primary_key=True, max_length=45)
    name = models.CharField(max_length=45)


class MediumCategory(models.Model):
    code = models.CharField(primary_key=True, max_length=45)
    name = models.CharField(max_length=45)


class SmallCategory(models.Model):
    code = models.CharField(primary_key=True, max_length=45)
    name = models.CharField(max_length=45)


class Area(models.Model):
    id = models.IntegerField(primary_key=True)
    gu = models.CharField(max_length=45)
    dong = models.CharField(max_length=45)
    dong_code = models.CharField(max_length=10)
    road_name = models.CharField(max_length=45)


class FootTraffic(models.Model):
    id = models.IntegerField(primary_key=True)

    road = models.ForeignKey(Area, on_delete=models.CASCADE)
    total_pcnt = models.IntegerField()
    
    men_pcnt = models.IntegerField()
    women_pcnt = models.IntegerField()

    teen_pcnt = models.IntegerField()
    twenty_pcnt = models.IntegerField()
    thirty_pcnt = models.IntegerField()
    fourty_pcnt = models.IntegerField()
    fifty_pcnt = models.IntegerField()
    sixty_pcnt = models.IntegerField()

    time1_pcnt = models.IntegerField()
    time2_pcnt = models.IntegerField()
    time3_pcnt = models.IntegerField()
    time4_pcnt = models.IntegerField()
    time5_pcnt = models.IntegerField()
    time6_pcnt = models.IntegerField()

    mon_pcnt = models.IntegerField()
    tue_pcnt = models.IntegerField()
    wed_pcnt = models.IntegerField()
    thr_pcnt = models.IntegerField()
    fri_pcnt = models.IntegerField()
    sat_pcnt = models.IntegerField()
    sun_pcnt = models.IntegerField()


class MeanSale(models.Model):
    id = models.IntegerField(primary_key=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)

    month = models.FloatField()
    week = models.FloatField()
    weekend = models.FloatField()
    mon = models.FloatField()
    tue = models.FloatField()
    wed = models.FloatField()
    thr = models.FloatField()
    fri = models.FloatField()
    sat = models.FloatField()
    sun = models.FloatField()
    time1 = models.FloatField()
    time2 = models.FloatField()
    time3 = models.FloatField()
    time4 = models.FloatField()
    time5 = models.FloatField()
    time6 = models.FloatField()
    men = models.FloatField()
    women = models.FloatField()
    teen = models.FloatField()
    twenty = models.FloatField()
    thirty = models.FloatField()
    fourty = models.FloatField()
    fifty = models.FloatField()
    sixty = models.FloatField()


class MeanSaleRate(models.Model):
    id = models.IntegerField(primary_key=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    week = models.FloatField()
    weekend = models.FloatField()
    mon = models.FloatField()
    tue = models.FloatField()
    wed = models.FloatField()
    thr = models.FloatField()
    fri = models.FloatField()
    sat = models.FloatField()
    sun = models.FloatField()
    time1 = models.FloatField()
    time2 = models.FloatField()
    time3 = models.FloatField()
    time4 = models.FloatField()
    time5 = models.FloatField()
    time6 = models.FloatField()
    men = models.FloatField()
    women = models.FloatField()
    teen = models.FloatField()
    twenty = models.FloatField()
    thirty = models.FloatField()
    fourty = models.FloatField()
    fifty = models.FloatField()
    sixty = models.FloatField()


class DevMeanSale(models.Model):
    id = models.IntegerField(primary_key=True)
    area = models.CharField(max_length=45)

    month = models.FloatField()
    week = models.FloatField()
    weekend = models.FloatField()
    mon = models.FloatField()
    tue = models.FloatField()
    wed = models.FloatField()
    thr = models.FloatField()
    fri = models.FloatField()
    sat = models.FloatField()
    sun = models.FloatField()
    time1 = models.FloatField()
    time2 = models.FloatField()
    time3 = models.FloatField()
    time4 = models.FloatField()
    time5 = models.FloatField()
    time6 = models.FloatField()
    men = models.FloatField()
    women = models.FloatField()
    teen = models.FloatField()
    twenty = models.FloatField()
    thirty = models.FloatField()
    fourty = models.FloatField()
    fifty = models.FloatField()
    sixty = models.FloatField()


class DevMeanSaleRate(models.Model):
    id = models.IntegerField(primary_key=True)
    area = models.CharField(max_length=45)
    week = models.FloatField()
    weekend = models.FloatField()
    mon = models.FloatField()
    tue = models.FloatField()
    wed = models.FloatField()
    thr = models.FloatField()
    fri = models.FloatField()
    sat = models.FloatField()
    sun = models.FloatField()
    time1 = models.FloatField()
    time2 = models.FloatField()
    time3 = models.FloatField()
    time4 = models.FloatField()
    time5 = models.FloatField()
    time6 = models.FloatField()
    men = models.FloatField()
    women = models.FloatField()
    teen = models.FloatField()
    twenty = models.FloatField()
    thirty = models.FloatField()
    fourty = models.FloatField()
    fifty = models.FloatField()
    sixty = models.FloatField()


class recommendResult(models.Model):
    id = models.IntegerField(primary_key=True)
    gu = models.CharField(max_length=45)
    dong = models.CharField(max_length=45)
    result = models.TextField()

