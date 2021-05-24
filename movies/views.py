
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator

from movies.forms import FilmModelForm
from movies.models import Film, Genre, Attachment
#from .forms import FilmForm


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


class FilmListView(ListView):
    model = Film

    context_object_name = 'films_list'   # your own name for the list as a template variable
    template_name = 'film/list.html'  # Specify your own template name/location
    paginate_by = 3

    def get_queryset(self):
        if 'genre_name' in self.kwargs:
            return Film.objects.filter(genres__name=self.kwargs['genre_name']).all() # Get 5 books containing the title war
        else:
            return Film.objects.all()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['num_films'] = len(self.get_queryset())
        if 'genre_name' in self.kwargs:
            context['view_title'] = f"Žánr: {self.kwargs['genre_name']}"
            context['view_head'] = f"Žánr filmu: {self.kwargs['genre_name']}"
        else:
            context['view_title'] = 'Filmy'
            context['view_head'] = 'Přehled filmů'
        return context

class FilmDetailView(DetailView):
    model = Film

    context_object_name = 'film_detail'   # your own name for the list as a template variable
    template_name = 'film/detail.html'  # Specify your own template name/location


class GenreListView(ListView):
    model = Genre
    template_name = 'blocks/genre_list.html'
    context_object_name = 'genres'
    queryset = Genre.objects.order_by('name').all()


class TopTenListView(ListView):
    model = Film
    template_name = 'blocks/top_ten.html'
    context_object_name = 'films'
    queryset = Film.objects.order_by('-rate').all()[:10]


class NewFilmListView(ListView):
    model = Film
    template_name = 'blocks/new_films.html'
    context_object_name = 'films'
    queryset = Film.objects.order_by('release_date').all()
    paginate_by = 2


class FilmCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Film
    fields = ['title', 'plot', 'release_date', 'runtime', 'poster', 'rate', 'genres']
    initial = {'rate': '5'}
    login_url = '/accounts/login/'
    permission_required = 'movies.add_film'


class FilmUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Film
    template_name = 'movies/film_bootstrap_form.html'
    form_class = FilmModelForm
    login_url = '/accounts/login/'
    permission_required = 'movies.change_film'


class FilmDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Film
    success_url = reverse_lazy('films')
    login_url = '/accounts/login/'
    permission_required = 'movies.delete_film'


def error_404(request, exception=None):
        return render(request, 'errors/404.html')

def error_500(request):
    return render(request, 'errors/500.html')

def error_403(request, exception=None):
    return render(request, 'errors/403.html')

def error_400(request, exception=None):
    return render(request, 'errors/400.html')

@never_cache
def clear_cache(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    cache.clear()
    return HttpResponse('Cache has been cleared')
