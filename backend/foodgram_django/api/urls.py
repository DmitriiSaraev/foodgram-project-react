from django.urls import include, path

from rest_framework import routers

from api.views import UserViewSet

app_name = 'api'

router_v1 = routers.SimpleRouter()
router_v1.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]

