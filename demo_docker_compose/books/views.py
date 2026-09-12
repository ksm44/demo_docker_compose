from django.shortcuts import render, redirect
from books.models import Book

def index(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        if title and author:
            Book.objects.create(title=title, author=author)
        return redirect('index')  # редирект для обновления страницы

    books = Book.objects.all()
    return render(request, 'index.html', {'books': books})