from django.urls import path
from api.views import UserEndPoint, EmailEndPoint, EmailVerifyEndPoint

urlpatterns = [
    path('users/me/', UserEndPoint.as_view({
        'get': 'retrieve',
        'patch': 'partial_update'
    }), name='retrieve_user'),
     path(
        'users/me/settings/',
        UserEndPoint.as_view(
            {
                "get": "retrieve_user_settings",
            }
        ),
        name="users",
    ),
    path('users/email/', EmailEndPoint.as_view(),),
    path('users/email/verify/', EmailVerifyEndPoint.as_view()),

]
