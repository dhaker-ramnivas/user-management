import logging
import coreschema
import jwt
import coreapi

from django.utils import timezone


from rest_framework_jwt import utils
from .utils import get_jwt_token,check_mandata

from .models import User,TextEntry


from rest_framework import status, serializers
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.schemas import AutoSchema

from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

from .notification import send_email_notification


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model=TextEntry,
        fields=('data',)


class UserRegister(GenericAPIView):
    renderer_classes = (JSONRenderer,)

    def post(self, request):
        """
            Creates a new user.
        """
        try:
            mandata=['username','email','password']
            check = check_mandata(request, mandata)

            if check[0] is False:
                return Response({"Message: %s " % (check[1])}, status=status.HTTP_400_BAD_REQUEST)
            user_email = request.data.get('email', None)
            user_username = request.data.get('username', None)
            user_password = request.data.get('password', None)
            try:
                user=User.objects.get(email=user_email)
            except User.DoesNotExist:
                user=None
            if user:
                return Response({"Error": "Email Id already Exist","status":False}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user=User.objects.create_user(username=user_username,email=user_email,password=user_password)
                user.is_active=False
                user.save()
                if user:

                    payload = utils.jwt_payload_handler(user)
                    token = utils.jwt_encode_handler(payload)

                    send_email_notification(receiver=user_email, token='?token=Bearer%20'+ token)
                    content = {
                        'user': {
                            'username': user.get_username(),
                            'email':user.email,
                            'message':'go to email and verify link'
                        },
                        "status":True
                        }
                    return Response(content, status=status.HTTP_201_CREATED)
                return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logging.exception(str(e))
            return Response({"Error":str(e),"status":False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserLogin(GenericAPIView):

    def get(self,request):
        try:

            user_email=request.query_params.get('email',None)
            user_password=request.query_params.get('password',None)


            if (user_email or user_password) is None:
                 return Response({'status': False,
                                'Error': 'Missing or incorrect credentials',
                                'data': request.query_params},
                                status=status.HTTP_400_BAD_REQUEST)
            try:
                user = User.objects.get(email=user_email,is_active=True)
            except User.DoesNotExist:
                return Response({'status': False,
                                 'Error': 'User not found',
                                 'data': request.query_params},
                                status=status.HTTP_404_NOT_FOUND)

            if not user.check_password(user_password):
                return Response({'status': False,
                                 'Error': 'Password is Incorrect ',
                                 'data': request.query_params},
                                status=status.HTTP_401_UNAUTHORIZED)

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            content = {
                    'username': user.get_username(),
                    'email': user.email,
                    'token': token
            }
            return Response({'status': True,
                             'message': 'Successfully logged in',
                             'user':content},
                            status=status.HTTP_200_OK)

        except Exception as e:
            logging.exception(str(e))
            return Response({"Error": str(e), "status": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ContentPost(GenericAPIView):
    def post(self, request):
        """
            Creates a new user.
        """
        try:
            mandata=['data']
            token = request.query_params.get('token', None)

            check = check_mandata(request, mandata)

            if check[0] is False:
                return Response({"Message: %s " % (check[1])}, status=status.HTTP_400_BAD_REQUEST)

            if token is not None:
                try:
                    payload = utils.jwt_decode_handler(get_jwt_token(token))
                    username = payload['username']
                    user = User.objects.get(username=username)
                    temp_id = payload['user_id']
                    if not (temp_id == user.id and user.get_username() == username):
                        return Response({"Error": "Unauthorized access", "status": False},
                                        status=status.HTTP_401_UNAUTHORIZED)
                except jwt.ExpiredSignatureError:
                    return Response({"Error": "Expired Token Signature", "status": False},
                                    status=status.HTTP_401_UNAUTHORIZED)
                except User.DoesNotExist:
                    return Response({"Error": "User not found", "status": False},
                                    status=status.HTTP_404_NOT_FOUND)

                content=request.data.get('data',None)

                if content:
                    user.textdata.create(data=content)
                    return Response({'status': True,
                                     'message': 'Successfully written data '},
                                     status=status.HTTP_200_OK)
            return Response({"Error": "Token Missing", "status": False},
                                    status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logging.exception(str(e))
            return Response({"Error":str(e),"status":False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ContentGet(GenericAPIView):
    def get(self,request):
        try:
            token = request.query_params.get('token', None)

            if token is not None:
                try:
                    payload = utils.jwt_decode_handler(get_jwt_token(token))
                    username = payload['username']
                    user = User.objects.get(username=username)
                    temp_id = payload['user_id']
                    if not (temp_id == user.id and user.get_username() == username):
                        return Response({"Error": "Unauthorized access", "status": False},
                                        status=status.HTTP_401_UNAUTHORIZED)
                except jwt.ExpiredSignatureError:
                    return Response({"Error": "Expired Token Signature", "status": False},
                                    status=status.HTTP_401_UNAUTHORIZED)
                except User.DoesNotExist:
                    return Response({"Error": "User not found", "status": False},
                                    status=status.HTTP_404_NOT_FOUND)

                queryset=TextEntry.objects.all()

                author_name=request.query_params.get('author',None)
                is_accending=int(request.query_params.get('is_accending',1))
                if author_name:
                    queryset=queryset.filter(user__username=author_name)
                if is_accending:
                    queryset=queryset.order_by('user__username')
                else:
                    queryset=queryset.order_by('-user__username')


                result=[]
                for data in queryset:
                    content={}
                    content["text"]=data.data
                    content["author"]=data.user.get_username()
                    result.append(content)


                return Response({'status': True,
                                     'data':result},
                                   status=status.HTTP_200_OK)
            return Response({"Error": "Unauthorized access", "status": False},
                            status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logging.exception(str(e))
            return Response({"Error":str(e),"status":False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserActivate(GenericAPIView):
    def get(self,request):

        try:
            token = request.query_params.get('token', None)

            if token is not None:
                try:
                    payload = utils.jwt_decode_handler(get_jwt_token(token))
                    username = payload['username']
                    user = User.objects.get(username=username)
                    temp_id = payload['user_id']
                    if not (temp_id == user.id and user.get_username() == username):
                        return Response({"Error": "Unauthorized access", "status": False},
                                        status=status.HTTP_401_UNAUTHORIZED)
                except jwt.ExpiredSignatureError:
                    return Response({"Error": "Expired Token Signature", "status": False},
                                    status=status.HTTP_401_UNAUTHORIZED)
                except User.DoesNotExist:
                    return Response({"Error": "User not found", "status": False},
                                    status=status.HTTP_404_NOT_FOUND)
            if user.is_active:
                return Response({'status': False,
                                 'message': 'please login with email',
                                 },status=status.HTTP_400_BAD_REQUEST)

            if user.is_active == False:
                if timezone.now() > user.profile.key_expires:
                    user.delete()
                    return Response({'status': False,
                                     'message': 'Please Register again',
                                     }, status=status.HTTP_401_UNAUTHORIZED)
                else:  # Activation successful
                    user.is_active = True
                    user.save()
                    return Response({'status': True,
                                 'message': 'Account Activated,please login with email',
                                 },status=status.HTTP_202_ACCEPTED)
            return Response({"Error": "Unauthorized access", "status": False},
                                        status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logging.exception(str(e))
            return Response({"Error": str(e), "status": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
