from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import EmailMessage
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import (
    UserCreateSerializer, UserSerializer, UserPasswordChangeSerializer,UserUpdateSerializer)
from .models import User
import random
# Create your views here.


@api_view(['POST'])
@permission_classes((AllowAny, ))
def user_signup(request):
    data = request.data
    serializer = UserCreateSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        user.set_password(request.data.get('password'))
        user.save()
        return Response({'message': '회원가입이 성공적으로 완료되었습니다.'})
    return Response(serializer.errors)

@api_view(['POST'])
@permission_classes((AllowAny,))
def email_check(request):
    data = request.data
    if User.objects.filter(email=data.get('email')):
        return Response({'message':'이미 존재하는 아이디', 'error':1})
    return Response({'message':'생성해도 됩니다.', 'error':0})

@api_view(['GET'])
@permission_classes((AllowAny, )) 
def user_detail(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes((AllowAny, ))
def find_email(request):
    users = User.objects.filter(nickname=request.data.get('nickname'), phone=request.data.get('phone'))
    if len(users)==0:
        return Response({'error':1, 'message':'NO User information !!'})
    else:
        em = []
        for user in users:
            em.append(
                user.email
            )          
    return Response({'email':em})

@api_view(['PUT'])
@permission_classes((AllowAny, )) 
def change_password(request,user_pk):
    if request.method=='PUT':
        user = get_object_or_404(User,pk=user_pk)
        serializer = UserPasswordChangeSerializer(data=request.data, instance=user)
        if serializer.is_valid():
            user=serializer.save()
            user.set_password(request.data.get('password'))
            user.save()
            return Response(serializer.data)
        return Response({'message': serializer.errors})


@api_view(['POST'])
@permission_classes((AllowAny,))
def find_password(request):
    user = User.objects.filter(nickname=request.data.get('nickname'), email=request.data.get('email'))
    if len(user) == 0:
        return Response({'error':1, 'message':'이름이랑 이메일이랑 일치하는 정보가 없다!!!'})
    user = user[0]
    a = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    random_password = ''
    for i in range(8):
        random_password += random.choice(a)
    random_password=random_password.upper()
    template = f'''
    관리자 입니다. 해당매일은 답장을 해도 반응이 없습니다.

    새로 발급받은 비밀 번호는 
    [{random_password}] 
    입니다. 로그인 후 비밀 번호 변경을 해주시기 바랍니다.
    '''
    mail = EmailMessage(
            f'[SSAFY_상새로이] {user.nickname}님의 새로 발급된 비밀번호 입니다.',
            template,
            to=[f'{user.email}']
        )
    mail.send() 
    serializer = UserPasswordChangeSerializer(data={'password':random_password}, instance=user)
    if serializer.is_valid():
        u = serializer.save()
        u.set_password(random_password)
        u.save()
    return Response({'error_message':serializer.errors,'message':'테스트할때 메일 안보내는걸로했어요. error_message가 비어있으면 정상적으로 작동합니다!!'})


@api_view(['PUT','DELETE'])
@permission_classes((AllowAny, ))
def user_update_delete(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    data = request.data
    if request.method == 'PUT':
        if not data.get('nickname'): data['nickname']=user.nickname
        if not data.get('business_exp'): data['business_exp']=user.business_exp
        if not data.get('phone'): data['phone']=user.phone
        if not data.get('interest_area'): data['interest_area']=user.interest_area
        serializer = UserUpdateSerializer(data=data, instance=user)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'error_message':serializer.errors, 'error':1})
    else:
        user.delete()
    return Response({'message':'user delete!!'})