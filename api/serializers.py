from rest_framework import serializers

from books.models import Book, BookReview
from users.models import CustomUser


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'isbn')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'email', 'username')


class BookReviewSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()
    book_id = BookSerializer()

    class Meta:
        model = BookReview
        fields = ('id', 'stars_given', 'comment', 'book_id', 'user_id',)