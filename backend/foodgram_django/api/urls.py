from django.urls import include, path, re_path

from rest_framework import routers

from api.views import UserViewSet, RecipeViewSet

app_name = 'api'

router_v1 = routers.SimpleRouter()
router_v1.register(r'users', UserViewSet)
router_v1.register(r'recipe', RecipeViewSet)

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router_v1.urls)),
]
