from django.urls import include, path, re_path

from rest_framework import routers
from rest_framework.authtoken import views
from djoser.views import UserViewSet as Set

from api.views import UserViewSet

app_name = 'api'

router_v1 = routers.SimpleRouter()
router_v1.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api-token-auth/', views.obtain_auth_token),
]

