from django.urls import include, path, re_path

from rest_framework import routers

from api.views import RecipeViewSet, TagViewSet, IngredientViewSet

app_name = 'api'

router = routers.SimpleRouter()
router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'ingredients', IngredientViewSet)

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
