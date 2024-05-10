
import uuid
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from db.models import User
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from api.helper import generate_token


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return (
        str(refresh.access_token),
        str(refresh),
    )

class SignUpEndpoint(APIView):

    def post(self, request):

        """
        Author: Mohammed Rifad on 10th March 2024
        Purpose: Registers a user.
        Input parameters: email, password 
        Return: Returns accessToken, refreshToken, message, statusCode

        """

        email = request.data.get("email", False)
        password = request.data.get("password", False)

        user = User.objects.filter(email=email)

        if not user.exists():
            encryped_password = make_password(password)
            user = User.objects.create(
                email=email, password=encryped_password, username=uuid.uuid4().hex)
            user.last_active = timezone.now()
            user.last_login_time = timezone.now()
            user.last_login_ip = request.META.get("REMOTE_ADDR")
            user.last_login_uagent = request.META.get("HTTP_USER_AGENT")
            user.token_updated_at = timezone.now()
            user.last_login = timezone.now()
            user.save()

            access_token, refresh_token = get_tokens_for_user(user)

            return Response(
                {
                    "accessToken": access_token,
                    "refreshToken": refresh_token,
                    'message': 'Hey! Account Created',
                    'statusCode': 201
                },
            )
        return Response(
            {
                'message': 'Email Exists',
                'statusCode': 409
            },
        )

class SignInEndPoint(APIView):

    def post(self, request):
         
        """
        Author: Mohammed Rifad on 10th March 2024
        Purpose: logs in a user.
        Input parameters: email, password 
        Return: Returns accessToken, refreshToken, message, statusCode
        
        """
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()

        if user is None:
            return Response(
                {
                    'message': 'Sorry, user not found. Please try again.',
                    'statusCode':  404
                },

            )
        if not check_password(password, user.password):
            print('password incorrect')

            return Response(
                {
                    'message': 'Password Incorrect',
                    'statusCode':  405
                },

            )

        user.last_active = timezone.now()
        user.last_login_time = timezone.now()
        user.last_login_ip = request.META.get("REMOTE_ADDR")
        user.last_login_uagent = request.META.get("HTTP_USER_AGENT")
        user.token_updated_at = timezone.now()
        user.save()

        access_token, refresh_token = get_tokens_for_user(user)
        
        data = {
            'accessToken': access_token,
            'refreshToken': refresh_token,
            'statusCode': 200,
             
        }
        response = Response(data)
        return response
