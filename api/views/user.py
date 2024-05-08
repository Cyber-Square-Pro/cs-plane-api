from rest_framework.views import APIView
from api.serializers.user import UserMeSerializer, UserMeSettingsSerializer, UserSerializer
from db.models import User, VerificationCode
from api.services import generate_verification_code
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from django.utils.decorators import method_decorator
from Plane.decorator import authorized
from django.http import HttpResponse



class UserEndPoint(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user_id
    
    def retrieve(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = UserMeSerializer(user)
        return Response(serializer.data)

    def retrieve_user_settings(self, request):
        user = User.objects.get(id = request.user.id)
        serialized_data = UserMeSettingsSerializer(user).data
        return Response(serialized_data, status=status.HTTP_200_OK)
    
    def partial_update(self, request):
        user = User.objects.get(id=request.user.id)
        print(request.data,'8888')
        serializer = UserMeSerializer(
            instance=user, data=request.data,  partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as e:
                print(e)

        return Response(serializer.data)

 
class EmailEndPoint(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            print('iii')
            user = User.objects.get(id=request.user.id)
            verification_code = generate_verification_code()
            user_record = VerificationCode.objects.filter(
                user=request.user.id).first()
            if not user_record:
                _ = VerificationCode.objects.create(
                    user=user, code=verification_code)

            else:
                user_record.code = verification_code
                user_record.created_at = timezone.now()
                user_record.save()
            return Response({
                'message': 'Verification code sent',
                'statusCode': 200,
                'code': verification_code,

            })

        except Exception as e:
            return Response({
                'message': 'Something Went Wrong',
                'statusCode': 409,

            })


 
class EmailVerifyEndPoint(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            print(request.data)
            code = request.data['code']

            user_record = VerificationCode.objects.get(user=request.user.id)

            if user_record.code == code:
                user = User.objects.get(id=request.user.id)
                user.onboarding_step['email_verified'] = True
                user.save()
                user_record.created_at = timezone.now()
                user_record.save()

                return Response({
                    'message': 'Email verified succesfully',
                    'statusCode': 200,
                })

            return Response({
                'message': 'Incorrect code',
                'statusCode': 405,
            })

        except Exception as e:
            print(e)
            return Response({
                'message': 'Something Went Wrong',
                'statusCode': 406,
            })


class CSTest(APIView):
    def get(self, request):
        return HttpResponse('Welcome to Plane App.....')