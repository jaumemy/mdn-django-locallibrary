from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic

# Create your views here.


def index(request):
    """View function for the home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default
    num_authors = Author.objects.count()

    # Generate count for genres
    num_genres = Genre.objects.count()

    # A list of books
    list_books = []
    str_books = ''
    for book in Book.objects.all():
        list_books.append(book.title)
    i = 0
    for book in list_books:
        if i == 0:
            str_books = book
        elif i == len(list_books)-1:
            str_books = str_books + ' and ' + book + '.'
        else:
            str_books = str_books + ', ' + book
        i += 1


    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'str_books': str_books,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)



class BookListView(generic.ListView):
    model = Book
    # paginate_by = 3
    # context_object_name = 'my_books_list' # your own name for the list as a template variable


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    # paginate_by = 3


class AuthorDetailView(generic.DetailView):
    model = Author
