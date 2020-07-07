from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from api import views
from django.urls import path

urlpatterns = [
    path('area/<area_gu>/', views.area_list),
    path('category/<medium>/', views.category_list),
    path('recommend/<gu>/<dong>/', views.recommend),
    path('analyze/<gu>/<dong>/', views.analyze ),
    path('analyze/<int:user_pk>/', views.user_analyze ),
    path('devsalerate/<station_name>/', views.dev_salerate),

]

