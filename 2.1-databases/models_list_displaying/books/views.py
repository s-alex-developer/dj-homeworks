from django.core.paginator import Paginator
from django.shortcuts import render, redirect


from .models import Book


def index(request):
    return redirect('books')


def books_view(request):

    template = 'books/books_list.html'

    context = {

        'books': [{'name': book.name, 'author': book.author, 'pub_date': book.pub_date, 'slug': book.slug}
                  for book in Book.objects.all()]

    }

    return render(request, template, context)


def pubdate_group_view(request, slug):

    template = 'books/pub_date.html'

    books = [{'name': book.name, 'author': book.author, 'pub_date': book.pub_date}
             for book in Book.objects.filter(slug=slug)]

    context = {

        'books': books,

    }

    return render(request, template, context)


