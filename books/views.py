from django.shortcuts import render
from django.views import View
from .models import Book


class BooksView(View):
    @staticmethod
    def get(request):
        books = Book.objects.all()
        context = {
            'books': books
        }
        return render(request, 'books/list.html', context)


class BookDetailView(View):
    @staticmethod
    def get(request, id):
        book = Book.objects.get(id=id)
        context = {
            'book': book
        }

        return render(request, 'books/detail.html', context)
