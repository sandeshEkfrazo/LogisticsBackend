from django.http.response import JsonResponse
import jwt
from rest_framework import authentication, exceptions, status
from account.models import *
from django.conf import settings
from rest_framework.response import Response
from jose.constants import ALGORITHMS
from datetime import datetime, timedelta
from django.conf import settings
import jwt

def generate_token(user_data):
    auth_token = jwt.encode({'user_id': '1', 'name': 'username', 'exp': datetime.utcnow() + timedelta(days=1)}, str(settings.JWT_SECRET_KEY), algorithm="HS256")
    return {
        'token': auth_token,
        'exipires': datetime.utcnow() + timedelta(days=1)
    }

def authorization_required(func):
    def checkAuthData(request, *args, **kwargs):
        try:
            if ('Authorization' in request.headers) and (len(request.headers['Authorization']) != 0):
                pass
            else:
                return JsonResponse({'error': {'code': 'AUTHENTICATION_FAILURE', 'message': 'You are not authorized to perform this operation. '}}, status=status.HTTP_401_UNAUTHORIZED)
            auth_data = request.headers['Authorization']
            if not auth_data:
                return JsonResponse(
                    {'error': {'code': 'INVALID_HEADER_FORMAT', 'message': 'you must be passed as Auth header '}}, status=status.HTTP_401_UNAUTHORIZED)
            if "Bearer " not in auth_data:
                return JsonResponse(
                    {'error': {'code': 'INVALID_TOKEN_FORMAT', 'message': 'check the token format '}}, status=status.HTTP_401_UNAUTHORIZED)
            auth_data = auth_data.split(' ')[1]

        except IndexError as e:
            return Response({'error': {'message': e}})

        try:
            # print(settings.SECRET_KEY, '======hello2====secret-key===========')
            payload = jwt.decode(auth_data, str(
                settings.JWT_SECRET_KEY), algorithms="HS256")
            payload_id = payload['user_id']
            user_id = CustomUser.objects.get(id=payload_id)
        except jwt.DecodeError as identifier:
            return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'You token is not valid'}}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.ExpiredSignatureError as identifier:
            return JsonResponse({'error': {"code": "AUTHENTICATION_FAILURE", 'message': 'token expired!,enter valid token'}}, status=status.HTTP_401_UNAUTHORIZED)

        return func(request, *args, **kwargs)
    return checkAuthData