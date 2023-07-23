from django.urls import path
from .views import BooksView, BookDetailView, AddReviewView, EditReviewView, ConfirmDeleteReviewView, DeleteReviewView

app_name = "books"
urlpatterns = [
    path('', BooksView.as_view(), name='books-list'),
    path('<int:id>/', BookDetailView.as_view(), name='books-detail'),
    path('<int:id>/review/', AddReviewView.as_view(), name='books-review'),
    path('<int:book_id>/reviews/<int:review_id>/edit/', EditReviewView.as_view(), name='reviews-edit'),
    path('<int:book_id>/reviews/<int:review_id>/delete/confirm', ConfirmDeleteReviewView.as_view(), name='review-confirm-delete'),
    path('<int:book_id>/reviews/<int:review_id>/delete/', DeleteReviewView.as_view(), name='review-delete')
]