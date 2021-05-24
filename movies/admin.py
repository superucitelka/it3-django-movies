from django.contrib import admin

# Import všech modelů, které obsahuje models.py
from django.db.models import Count
from django.utils.html import format_html

from .models import *

# Registrace modelů v administraci aplikace
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "film_count")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _film_count=Count("film", distinct=True),
        )
        return queryset

    def film_count(self, obj):
        return obj._film_count

    film_count.admin_order_field = "_film_count"
    film_count.short_description = "Počet filmů"


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ("title", "release_year", "rate_percent")

    def release_year(self, obj):
        return obj.release_date.year

    def rate_percent(self, obj):
        return format_html("<b>{} %</b>", int(obj.rate * 10))

    rate_percent.short_description = "Hodnocení filmu"
    release_year.short_description = "Rok uvedení"


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "filesize", "film_title")

    def film_title(self, obj):
        return obj.film.title


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("author", "film", "rate", "edit_date")