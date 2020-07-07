from django.urls import path,include
from rest_framework_jwt.views import obtain_jwt_token
from accounts import views 
urlpatterns = [
    path('login/', obtain_jwt_token),
    path('signup/', views.user_signup),
    path('userdetail/<int:user_pk>/', views.user_detail),
    path('user/<int:user_pk>/updatedelete/', views.user_update_delete),
    path('email-check/', views.email_check),
    path('changepassword/<int:user_pk>/', views.change_password),
    path('findemail/', views.find_email),
    path('findpassword/', views.find_password),
]