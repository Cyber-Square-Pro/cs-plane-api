import functools
from django.http import JsonResponse
import jwt
from db.models import User
from django.conf import settings


def authorized(function):
    @functools.wraps(function)
    def wrap(request, *args, **kwargs):

        auth_header = request.META.get('HTTP_AUTHORIZATION')
        print('auth', auth_header)
        if 'HTTP_AUTHORIZATION' in request.META:
            token = auth_header.split('Bearer ')[1]
            try:
                # Verify and decode the JWT token
                decode_token = jwt.decode(
                    token, settings.JWT_SECRET, algorithms=['HS256'])

                # Add the decoded token to the request object
                print('di', decode_token)
                request.user = User.objects.get(pk = decode_token['id'])
                print('dssi', decode_token)
                return function(request, *args, **kwargs)
            except Exception as e:
                print('errrrrrrrr', e)
                None

    return wrap
