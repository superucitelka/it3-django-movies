from django.shortcuts import render


def index(request):
    """
    View function for home page of site.
    """
    # Render the HTML template index.html
    return render(
        request,
        'index.html',
    )

def topten(request):
    """
    View function for home page of site.
    """
    # Render the HTML template index.html
    return render(
        request,
        'topten.html',
    )

