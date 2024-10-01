from typing import Any
from django.shortcuts import render, redirect, get_object_or_404  # type: ignore
from django.views.generic import ListView, DetailView  # type: ignore
from .models import Recipe
from .utils import (
    get_top_ingredients_chart,
    get_difficulty_spread_chart,
    get_cooking_time_by_difficulty_chart,
)
from django.http import JsonResponse #type:ignore
from django.contrib.auth.mixins import LoginRequiredMixin  # type: ignore
from .forms import RecipeSearchForm, RecipeForm
import pandas as pd  # type: ignore
import json
from django.views.decorators.http import require_POST, require_http_methods #type:ignore
from django.contrib.auth.decorators import login_required #type:ignore
from json.decoder import JSONDecodeError
from django.contrib import messages #type:ignore
from django.conf import settings #type:ignore
import os


# Create your views here.
def home(request):
    return render(request, "recipes/recipes_home.html")


class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = "recipes/recipes_overview.html"

    # recipe search view
    def get_queryset(self):
        queryset = super().get_queryset()

        # retrieve search parameters
        recipe_name = self.request.GET.get("recipe_name")
        ingredient = self.request.GET.get("ingredient")
        difficulty = self.request.GET.get("difficulty")

        # filter queryset based on search parameters
        if recipe_name:
            queryset = queryset.filter(name__icontains=recipe_name)
        if ingredient:
            queryset = queryset.filter(ingredients__icontains=ingredient)
        if difficulty and difficulty != "":
            queryset = queryset.filter(difficulty=difficulty)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        df = pd.DataFrame(list(queryset.values("id", "name", "pic", "cooking_time")))
        recipes = df.to_dict("records") if not df.empty else []
        for recipe in recipes:
            recipe_instance = Recipe.objects.get(pk=recipe["id"])
            recipe["get_absolute_url"] = recipe_instance.get_absolute_url()
            recipe["pic_url"] = recipe_instance.pic.url if recipe_instance.pic else None

        # Adds the modified list of recipes to the context.
        context["object_list"] = recipes
        num_results = len(context["object_list"])
        title_parts = []

        # retrieve search parameters
        recipe_name = self.request.GET.get("recipe_name")
        ingredient = self.request.GET.get("ingredient")
        difficulty = self.request.GET.get("difficulty")

        if recipe_name:
            title_parts.append(f"'{recipe_name}' in the name")
        if ingredient:
            title_parts.append(f"'{ingredient}' in ingredients")
        if difficulty and difficulty != "":
            title_parts.append(f"difficulty of {difficulty}")

        # Constructing the main title and detailed search criteria
        if title_parts:
            context["main_title"] = "Results for:"
            recipe_word = "Recipe" if num_results == 1 else "Recipes"
            details_intro = (
                f"{recipe_word} with "  # Adjust the intro based on number of results
            )
            context["search_details"] = details_intro + ", ".join(title_parts)
        else:
            context["main_title"] = "Full List of Recipes"
            context["search_details"] = ""

        # Additional context for search form and charts based on the filtered recipes.
        # recipes_list = list(queryset.values('id', 'name', 'ingredients', 'description', 'pic', 'cooking_time', 'difficulty'))
        context["search_form"] = RecipeSearchForm(
            self.request.GET
        )  # Retain the search form input
        context["show_all_recipes_button"] = bool(self.request.GET)

        # adds charts to context
        recipes_list = list(
            queryset.values(
                "id", "name", "ingredients", "pic", "cooking_time", "difficulty"
            )
        )
        context["top_ing_chart"] = get_top_ingredients_chart(recipes_list)
        context["difficulty_spread_chart"] = get_difficulty_spread_chart(recipes_list)
        context["difficulty_and_time_chart"] = get_cooking_time_by_difficulty_chart(
            recipes_list
        )

        return context


class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = "recipes/recipe_details.html"


@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the valid form and return a success status
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            # Return form errors as JSON if form is not valid
            return JsonResponse({'status': 'error', 'errors': form.errors})
    # Handle non-POST methods
    return JsonResponse({'status': 'invalid_method'})


@login_required
def update_recipe(request, pk):
    #retrieve selected recipe
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)

        if form.is_valid():
            form.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'message': 'Recipe updated successfully!'}, status=200)
            else:
                return redirect('recipes:detail', pk=recipe.pk)  # Redirect to a recipe detail view
        else:
            # Handle form errors for AJAX requests
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # Send the form errors in JSON format
                return JsonResponse({'errors': form.errors}, status=400)
    else:
        # For GET request, pre-populate the form with the existing recipe data
        form = RecipeForm(instance=recipe)
    
    # Render the form (for non-AJAX requests or in case of GET request)
    return render(request, 'recipes/recipe_details.html', {'form': form, 'object': recipe})

    

@login_required
@require_POST
def delete_recipe(request, pk):
    try:
        recipe = get_object_or_404(Recipe, pk=pk)
        recipe.delete()
        return JsonResponse({'status': 'success'})
    except JSONDecodeError:
        # Handle cases where the request body does not contain valid JSON
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)