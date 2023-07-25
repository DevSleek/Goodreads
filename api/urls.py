from .views import BookReviewViewSet
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register('reviews', BookReviewViewSet, basename='review')

urlpatterns = router.urls
