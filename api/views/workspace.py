from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from api.serializers import WorkSpaceSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from db.models import Workspace, WorkspaceMember
from rest_framework import status
from .base import BaseAPIView
from db.models import User
from django.db.models import (
    Prefetch,
    OuterRef,
    Func,
    F,
)
from django.utils.decorators import method_decorator
from Plane.decorator import authorized

 
class WorkspaceEndpoint(viewsets.ViewSet, BaseAPIView):
    permission_classes = [IsAuthenticated]
    def fetch_workspace(self, request):
        member_count = (
            WorkspaceMember.objects.filter(
                workspace=OuterRef("id"), member__is_bot=False
            )
            .order_by()
            .annotate(count=Func(F("id"), function="Count"))
            .values("count")
        )
        workspace = (
            (
                Workspace.objects.prefetch_related(
                    Prefetch("workspace_member", queryset=WorkspaceMember.objects.all())
                )
                .filter(
                    workspace_member__member=request.user.id,
                )
                .select_related("owner")
            )
            .annotate(total_members=member_count)
            
        )
        

        serializer = WorkSpaceSerializer(self.filter_queryset(workspace), many=True)
        print(serializer.data)
        return Response({
            'data':serializer.data, })
    
    def create(self, request):
        try:
            
            slug = request.data['slug']
            workspace_name = request.data['name']
            organization_size = request.data['organization_size']
            serializer = WorkSpaceSerializer(data=request.data)
            workspace_slug = Workspace.objects.filter(slug = slug).exists()
            if workspace_slug:
                return Response(
                    {'status_code': 409, 
                     'message': 'Workspace URL is already taken!'
                     }) 
             
            if not workspace_name or not slug:
                return Response(
                    {'message': "Both name and slug are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            if len(workspace_name) > 80 or len(slug) > 48:
                return Response(
                    {'message': "The maximum length for name is 80 and for slug is 48"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
            if serializer.is_valid():
                serializer.save(owner_id = request.user.id)
                workspace = WorkspaceMember.objects.create(
                    workspace_id=serializer.data["id"],
                    member_id=request.user.id,
                    role=20,
                    
                )
                
                user = User.objects.get(id = request.user.id)
                user.is_onboarded = True
                print('id is', workspace.id)
                print('actual',serializer.data["id"] )
                user.last_workspace_id = serializer.data["id"]
                user.onboarding_step['workspace_create'] = True
                user.save()

                # token_response = self.handle_token_response(request)
                return Response({
                    'data':serializer.data,
                    'message': 'Workspace Created Succesfully',
                    })
            else:
                return Response({
                    'data':serializer.data,
                    'message': 'Form Error',
                    })
        except :
           return Response({
                    'data':serializer.data,
                    'message': 'Something Went Wrong',
                    })

 
class WorkSpaceAvailabilityCheckEndpoint(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        slug = request.GET.get("slug", False)

        if not slug or slug == "":
            return Response({
                'message': 'Workspace Slug is required',
                'statusCode': 400
                })
        
        workspace = Workspace.objects.filter(slug=slug).exists()
        return Response({
            'status':not workspace,
            'statusCode': 200
             })
