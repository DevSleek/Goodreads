from django.test import TestCase
from django.urls import reverse
from books.models import Book


class BooksTestCase(TestCase):
    def test_no_book(self):
        response = self.client.get(reverse('books:books-list'))

        self.assertContains(response, "No books found.")

    def test_books_list(self):
        book1 = Book.objects.create(title='Book1', description='description1', isbn='111111')
        book2 = Book.objects.create(title='Book2', description='description2', isbn='222222')
        book3 = Book.objects.create(title='Book3', description='description3', isbn='333333')

        response = self.client.get(reverse('books:books-list') + '?page_size=2')

        for book in [book1, book2]:
            self.assertContains(response, book.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:books-list') + '?page=2&page_size=2')

        self.assertContains(response, book3.title)

    def test_detail_page(self):
        book = Book.objects.create(title='Book1', description='description1', isbn='111111')

        response = self.client.get(reverse('books:books-detail', kwargs={'id': book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)





