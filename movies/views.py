from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator

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


class FilmCreate(CreateView):
    model = Film
    fields = ['title', 'plot', 'release_date', 'runtime', 'poster', 'rate', 'genres']
    initial = {'rate': '5'}


class FilmUpdate(UpdateView):
    model = Film
    fields = '__all__' # Not recommended (potential security issue if more fields added)


class FilmDelete(DeleteView):
    model = Film
    success_url = reverse_lazy('films')