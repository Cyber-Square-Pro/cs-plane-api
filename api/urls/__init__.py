from .authentication import urlpatterns as authentication_urls
from .user import urlpatterns as user_urls
from .workspace import urlpatterns as workspace_urls


urlpatterns = [
    *authentication_urls,
    *user_urls,
    *workspace_urls
]
