from .base import BaseSerializer
from .user import UserLiteSerializer
from rest_framework import serializers
from db.models import Workspace

class WorkSpaceSerializer(BaseSerializer):
    owner = UserLiteSerializer(read_only = True)
    total_members = serializers.IntegerField(read_only = True)
    total_issues = serializers.IntegerField(read_only =True)

    class Meta:
        model = Workspace
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
            "owner",
        ]

class WorkspaceLiteSerializer(BaseSerializer):
    class Meta:
        model = Workspace
        fields = [
            "name",
            "slug",
            "id",
        ]
        read_only_fields = fields
