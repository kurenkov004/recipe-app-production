from django.urls import path #type:ignore
from .views import home, RecipeListView, RecipeDetailView, add_recipe, update_recipe, delete_recipe
from django.views.decorators.csrf import csrf_exempt #type:ignore

app_name = "recipes"

urlpatterns = [
    path("", home),
    path("list/", RecipeListView.as_view(), name="list"),
    path("list/<pk>", RecipeDetailView.as_view(), name="detail"),
    path("about/", home, name="about"),
    path("add/", add_recipe, name="add_recipe"),
    path('update/<pk>/', update_recipe, name='update_recipe'),
    path('delete/<pk>/', csrf_exempt(delete_recipe), name='delete_recipe'), #exempt from CSRF checks, using 'pk' as a placeholder for the recipe ID
]
