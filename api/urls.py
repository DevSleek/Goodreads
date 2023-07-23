from .views import BookReviewDetailAPIView, BookReviewsListAPIView
from django.urls import path

app_name = 'api'
urlpatterns = [
    path('reviews/', BookReviewsListAPIView.as_view(), name='review-list'),
    path('reviews/<int:id>/', BookReviewDetailAPIView.as_view(), name='review-detail-api')
]