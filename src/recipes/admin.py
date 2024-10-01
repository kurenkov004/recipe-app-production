# from django.contrib import admin
# from .models import Recipe

# # Register your models here.
# admin.site.register(Recipe)

from django.contrib import admin #type:ignore
from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "cooking_time", "difficulty")
    readonly_fields = ("difficulty",)
