"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
        title='big_data_api',
        default_version='v1',
        # 아래 주석은 선택 인자입니다.
        # description="음악관련 API 서비스입니다.",
        # terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(email="edujunho.hphk@gmail.com"),
        # license=openapi.License(name="SSAFY License"),
   ),
)
urlpatterns = [
    path("dc/admin/", admin.site.urls),
    path("dc/api/", include("api.urls")),
    path("dc/accounts/", include("accounts.urls")),
    path("dc/boards/",include("boards.urls")),
    path('dc/redocs/', schema_view.with_ui('redoc'), name='api_docs'),
    path('dc/swagger/', schema_view.with_ui('swagger'), name='api_swagger'),
]
