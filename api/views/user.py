from rest_framework.views import APIView
from api.serializers.user import UserMeSerializer, UserMeSettingsSerializer, UserSerializer
from db.models import User, VerificationCode
from api.utils import generate_verification_code, send_otp
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

        """
        Author: Mohammed Rifad on 21st April 2024
        Purpose: Retrieves user details.
        Input parameters: None
        Return: Returns {'id', 'avatar', 'cover_image', 'date_joined',
                'display_name', 'email', 'first_name', 'last_name','is_active',
                'is_bot', 'is_email_verified', 'is_managed', 'is_onboarded', 
                'is_tour_completed','mobile_number','role', 'onboarding_step',
                'user_timezone', 'username', 'theme', 'last_workspace_id'}

        """

        user = User.objects.get(id=request.user.id)
        serializer = UserMeSerializer(user)
        return Response(serializer.data)

    def retrieve_user_settings(self, request):
         
        """
        Author: Mohammed Rifad on 21st April 2024
        Purpose: Retrieves user settings.
        Input parameters: None
        Return: Returns {'id', 'email', 'workspace'}

        """
        user = User.objects.get(id = request.user.id)
        serialized_data = UserMeSettingsSerializer(user).data
        return Response(serialized_data, status=status.HTTP_200_OK)
    
    def partial_update(self, request):

        """
        Author: Mohammed Rifad on 23rd April 2024
        Purpose: Updates user data 
        Input parameters: User field that needs to be updated like workspace, profile etc
        Return: Returns {'id', 'email', 'workspace'}

        """
        user = User.objects.get(id=request.user.id)
        serializer = UserMeSerializer(
            instance=user, data=request.data,  partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as e:
                None

        return Response(serializer.data)

 
class EmailEndPoint(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
         
        """
        Author: Mohammed Rifad on 25th April 2024
        Purpose: Sends Verification code to user's email.
        Input parameters: None
        Return: Returns {'message', 'statusCode}

        """

        try:
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
                
                # Added by Fidha Naushad on 11th May 2024 - previously code was being displayed on the browser's console 
                send_otp(
                    email_subject = 'Email Verification',
                    email_template = 'email_verification.html',
                    recipient_email = user.email,
                    context = {'verification_code' : verification_code }
                )
                  
            return Response({
                'message': 'Verification code has been sent to your email',
                'statusCode': 200,
                'code': verification_code,

            })

        except Exception as e:
            print(e)
            return Response({
                'message': 'Something Went Wrong',
                'statusCode': 409,

            })


 
class EmailVerifyEndPoint(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):

        """
        Author: Mohammed Rifad on 27th April 2024
        Purpose: Verifies user email by checking OTP.
        Input parameters: OTP
        Return: Returns {'message', 'statusCode'}

        """

        try:
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

            return Response({
                'message': 'Something Went Wrong',
                'statusCode': 406,
            })


class CSTest(APIView):
    def get(self, request):
        return HttpResponse('Hello from Plane App..')