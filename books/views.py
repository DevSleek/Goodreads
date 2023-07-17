from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse

from .forms import BookReviewForm
from .models import Book, BookReview


class BooksView(View):
    @staticmethod
    def get(request):
        books = Book.objects.all().order_by('id')
        search_query = request.GET.get('q')
        if search_query:
            books = books.filter(title__icontains=search_query)

        page_size = request.GET.get('page_size', 2)
        paginator = Paginator(books, page_size)
        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)
        context = {
            'page_obj': page_obj
        }
        return render(request, 'books/list.html', context)

# PAGINATOR GenericVIEW ---> paginate_by = NUMBER


class BookDetailView(View):
    @staticmethod
    def get(request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm()
        context = {
            'book': book,
            'review_form': review_form
        }

        return render(request, 'books/detail.html', context)


class AddReviewView(LoginRequiredMixin, View):
    @staticmethod
    def post(request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm(data=request.POST)

        if review_form.is_valid():
            BookReview.objects.create(
                book_id=book,
                user_id=request.user,
                stars_given=review_form.cleaned_data['stars_given'],
                comment=review_form.cleaned_data['comment']
            )

            return redirect(reverse('books:books-detail', kwargs={'id': book.id}))

        else:
            context = {
                'book': book,
                'review_form': review_form
            }

            return render(request, 'books/detail.html', context)

