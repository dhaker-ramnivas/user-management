from django.conf import settings
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from django.utils.encoding import smart_text
from django.utils.translation import ugettext as _
from rest_framework import exceptions
from rest_framework import HTTP_HEADER_ENCODING
from django.utils.six import text_type
from django import utils
from .models import User
import jwt


class JSONWebTokenAuthenticationQS(JSONWebTokenAuthentication):

    def get_jwt_value(self, request):

        auth = request.query_params.get('token', b'').split()
        if isinstance(auth, text_type):
            # Work around django test client oddness
            auth = auth.encode(HTTP_HEADER_ENCODING)

        auth_header_prefix = api_settings.JWT_AUTH_HEADER_PREFIX.lower()

        if not auth:
            if api_settings.JWT_AUTH_COOKIE:
                return request.COOKIES.get(api_settings.JWT_AUTH_COOKIE)
            return None

        if smart_text(auth[0].lower()) != auth_header_prefix:
            return None

        if len(auth) == 1:
            msg = _('Invalid Authorization header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid Authorization header. Credentials string '
                    'should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        return auth[1]


def get_jwt_token(payload):
    prefix = settings.JWT_AUTH.get('JWT_AUTH_HEADER_PREFIX').lower()
    if payload.lower().startswith(prefix):
        return payload.split(' ')[1]
    else:
        raise Exception('malformed jwt token')


def check_mandata(request,mandata):
    request_data=request.data
    for mandata_key in mandata:
        if mandata_key not in request_data.keys():
            return False,mandata_key+" is missing"
    request_value=list(request_data.values())

    for value in request_value:
        if type(value) == list:
            if len(value) == 0:
                return False,"some value(s) are empty,try again"
        elif type(value) == str:
            if len(value.strip()) == 0:
                return False,"some value(s) are empty,try again"
        elif type(value) == dict:
            if bool(value)==False:
                return False, "some value(s) are empty,try again"
    return True,None
