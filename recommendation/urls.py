from rest_framework.routers import DefaultRouter
from recommendation.views import RecommendationViewSet, RecommendationSettings

router = DefaultRouter()

router.register(r'recommendation', RecommendationViewSet, basename='recommendation')
router.register(r'recommendation-settings', RecommendationSettings, basename='recommendation-settings')
