import json
import requests

from django.views import View
from django.http import JsonResponse,HttpResponse

class KakaoLoginView(View):
    def get(self, request):
        kakao_access_code=request.GET.get('code',None)

        url="https://kauth.kakao.com/oauth/token"

        headers={'Content-type':'application/x-www-form-urlencoded; charset=utf-8'}

        body={'grant_type':'authorization_code',
              'client_id':'34aeeae559700e31f981b70970a7b2d2',
              'redirect_uri':'http://127.0.0.1:8000/accounts',
              'code':kakao_access_code
        }

        token_kakao_reponse = requests.post(url,headers=headers,data=body)
        access_token        = json.loads(token_kakao_reponse.text).get('access_token')

        url = 'https://kapi.kakao.com/v2/user/me'

        headers = {
            'Authoriztion':f'Bearer {access_token}',
            'Content-type':'application/x-www-form-urlencoded; charset=utf-8'
        }

        kakao_response =requests.get(url,headers=headers)
        
        return HttpResponse(f'{kakao_response.text}')  
