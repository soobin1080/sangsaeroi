from .models import DevMeanSale, DevMeanSaleRate
from rest_framework import serializers


class DevMeanSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevMeanSale
        fields = '__all__'


class DevMeanSaleRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevMeanSaleRate
        fields = '__all__'