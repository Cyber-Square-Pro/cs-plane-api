from rest_framework import serializers
from db.models import User,Workspace
from .base import BaseSerializer
from rest_framework import serializers

class UserEmailSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = User
        fields = ('email',)

class UserLiteSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "avatar",
            "is_bot",
            "display_name",
        ]
        read_only_fields = [
            "id",
            "is_bot",
        ]
class UserSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "is_superuser",
            "is_staff",
            "last_active",
            "last_login_time",
            "last_logout_time",
            "last_login_ip",
            "last_logout_ip",
            "last_login_uagent",
            "token_updated_at",
            "is_onboarded",
            "is_bot",
        ]

class UserMeSettingsSerializer(BaseSerializer):
    workspace = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "workspace",
        ]
        read_only_fields = fields

    def get_workspace(self, obj):
        # workspace_invites = WorkspaceMemberInvite.objects.filter(
        #     email=obj.email
        # ).count()
        if obj.last_workspace_id is not None:
            workspace = Workspace.objects.filter(
                pk=obj.last_workspace_id, workspace_member__member=obj.id
            ).first()
            return {
                "last_workspace_id": obj.last_workspace_id,
                "last_workspace_slug": workspace.slug if workspace is not None else "",
                "fallback_workspace_id": obj.last_workspace_id,
                "fallback_workspace_slug": workspace.slug if workspace is not None else "",
                # "invites": workspace_invites,
            }
        else:
            fallback_workspace = (
                Workspace.objects.filter(workspace_member__member_id=obj.id)
                 
                .first()
            )
            return {
                "last_workspace_id": None,
                "last_workspace_slug": None,
                "fallback_workspace_id": fallback_workspace.id
                if fallback_workspace is not None
                else None,
                "fallback_workspace_slug": fallback_workspace.slug
                if fallback_workspace is not None
                else None,
                # "invites": workspace_invites,
            }

class UserMeSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "avatar",
            "cover_image",
            "date_joined",
            "display_name",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_bot",
            "is_email_verified",
            "is_managed",
            "is_onboarded",
            "is_tour_completed",
            "mobile_number",
            "role",
            "onboarding_step",
            "user_timezone",
            "username",
            "theme",
            "last_workspace_id",
        ]
        