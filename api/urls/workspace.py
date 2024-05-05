from django.urls import path
from api.views import WorkspaceEndpoint, WorkSpaceAvailabilityCheckEndpoint

urlpatterns = [
    path('users/me/workspaces/', WorkspaceEndpoint.as_view({
        'get': 'fetch_workspace',
        'post': 'create'
    }), name='create_workspace'),

    path('workspaces/slug-check/',
         WorkSpaceAvailabilityCheckEndpoint.as_view(), name='workspace-availability')


]
