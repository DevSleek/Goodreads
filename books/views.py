from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from .models import Book


class BooksView(View):
    @staticmethod
    def get(request):
        books = Book.objects.all().order_by('id')
        page_size = request.GET.get('page_size', 2)
        paginator = Paginator(books, page_size)
        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)
        context = {
            # 'books': books,
            'page_obj': page_obj
        }
        return render(request, 'books/list.html', context)

# PAGINATOR GenericVIEW ---> paginate_by = NUMBER


class BookDetailView(View):
    @staticmethod
    def get(request, id):
        book = Book.objects.get(id=id)
        context = {
            'book': book
        }

        return render(request, 'books/detail.html', context)
