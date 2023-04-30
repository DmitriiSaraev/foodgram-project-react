from django.urls import include, path, re_path

from rest_framework import routers

from api.views import RecipeViewSet, TagViewSet, IngredientViewSet, \
    SubscriptionsViewSet, SubscribeViewSet

app_name = 'api'

router = routers.SimpleRouter()
router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'users/subscriptions', SubscriptionsViewSet, basename='users/subscriptions')
router.register(r'users/subscribe', SubscribeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'users/<int:pk>/subscribe/',
        SubscribeViewSet.as_view({'post': 'subscribe', 'delete': 'subscribe'})
    ),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    # path('', include(router.urls)),
]

