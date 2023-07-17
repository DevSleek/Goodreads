from django.urls import path
from .views import BooksView, BookDetailView, AddReviewView

app_name = "books"
urlpatterns = [
    path('', BooksView.as_view(), name='books-list'),
    path('<int:id>/', BookDetailView.as_view(), name='books-detail'),
    path('<int:id>/review/', AddReviewView.as_view(), name='books-review')
]