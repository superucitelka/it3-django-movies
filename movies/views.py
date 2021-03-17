from django.shortcuts import render
from movies.models import Film, Genre, Attachment

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_films = Film.objects.all().count()
    films = Film.objects.order_by('-rate')[:3]

    context = {
        'num_films': num_films,
        'films': films
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def topten(request):
    """
    View function for home page of site.
    """
    # Render the HTML template index.html
    return render(
        request,
        'topten.html',
    )

