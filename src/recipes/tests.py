from django.test import TestCase  # type: ignore
from .models import Recipe
from django.urls import reverse #type:ignore
from django.contrib.auth.models import User #type:ignore
from .forms import RecipeSearchForm, RecipeForm
import json


# Create your tests here.
class RecipeModelTest(TestCase):

    def setUpTestData():
        # set up non-modified objects used by all test methods
        Recipe.objects.create(
            name="Test Recipe",
            ingredients="Tea leaves, Water",
            cooking_time=5,
            difficulty="Easy",
        )

    # ------------------------------NAME TESTS------------------------------#
    def test_recipe_name(self):
        # get a recipe object to test
        recipe = Recipe.objects.get(id=1)
        # get metadata for the 'name' field and use it to query its data
        field_label = recipe._meta.get_field("name").verbose_name
        # compare value to expected result
        self.assertEqual(field_label, "name")

    def test_recipe_name_length(self):
        # get a recipe object to test
        recipe = Recipe.objects.get(id=1)
        # get metadata for the 'name' field and use it to query its data
        max_length = recipe._meta.get_field("name").max_length
        # compare value to expected result
        self.assertEqual(max_length, 50)

    # ------------------------------INGREDIENTS TESTS------------------------------#
    def test_igredients_max_length(self):
        # get a recipe object to test
        recipe = Recipe.objects.get(id=1)
        # get metadata for 'ingredients' field and use it to query its data
        max_length = recipe._meta.get_field("ingredients").max_length
        # compare values
        self.assertEqual(max_length, 225)

    # ------------------------------COOKING TIME TESTS------------------------------#
    def test_cooking_time_data_type(self):
        # get a recipe object to test
        recipe = Recipe.objects.get(id=1)
        # get metadata for 'cooking_time' field and use it to query its data
        cooking_time_input = recipe.cooking_time
        # compare values
        self.assertIsInstance(cooking_time_input, int)

    # ------------------------------DIFFICULTY TESTS------------------------------#
    def test_difficulty_calc(self):
        # get a recipe object to test
        recipe = Recipe.objects.get(id=1)
        # compare values
        self.assertEqual(recipe.calculate_difficulty(), "Easy")

    # ------------------------------MISC TESTS------------------------------#  
    def test_default_img_path(self):
        # Verifies that the default path for a recipe's image is correctly set.
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.pic, 'no_picture.jpg')


class SearchFormTest(TestCase):

    # tests validity of the Search Form

    def test_form_validity(self):
        # set up test data & test form validity
        form_data = {
            "recipe": "coffee",
            "ingredient": "water",
            "difficulty": "Easy",
        }

        form = RecipeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

        form_data_partial = {
            "recipe": "coffee",
            "difficulty": "Easy",
        }
        form_partial = RecipeSearchForm(data=form_data_partial)
        self.assertTrue(form_partial.is_valid())


class RecipeModelMethodTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="12345")
        cls.recipe = Recipe.objects.create(
            name="Test Recipe Methods",
            ingredients="Ing1, Ing2, Ing3",
            cooking_time=5,
            difficulty="Easy",
        )

    def test_get_absolute_url(self):
        # Ensures the method correctly returns the absolute URL for a recipe detail view.
        expected_url = reverse("recipes:detail", kwargs={"pk": self.recipe.pk})
        self.assertEqual(self.recipe.get_absolute_url(), expected_url)


class RecipeViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="12345")
        cls.recipe = Recipe.objects.create(
            name="Test Recipe Views",
            ingredients="Ing1, Ing2, Ing3",
            cooking_time=5,
            difficulty="Easy",
        )

    def test_login_required_for_list_view(self):
        # Checks if accessing the list view without authentication correctly redirects to the login page.
        response = self.client.get("/list/")
        self.assertRedirects(response, "/login/?next=/list/")

    # def test_login_required_for_detail_view(self):
    #     # ensures the detail view requires user authentication.
    #     response = self.client.get(f'/list/{self.recipe.pk}/')
    #     self.assertRedirects(response, f'/login/?next=/list/{self.recipe.pk}/')

    def test_home_page_status_code(self):
        # Verifies that the home page is accessible and returns the correct HTTP status code.
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_recipe_list_view(self):
        # Tests accessibility of the recipe list view when logged in.
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("recipes:list"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_view(self):
        # Confirms that the recipe detail view is accessible for an existing recipe when logged in.
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("recipes:detail", args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 200)

class RecipeFormTest(TestCase):

    def test_recipe_form_valid(self):
        #provide valid data
        form_data = {
            'name': 'Test',
            'ingredients': 'Ing1, ing2, ing3',
            'cooking_time': 5,
        }
        form = RecipeForm(data=form_data)

        # Ensure the form is valid
        self.assertTrue(form.is_valid())
        # Test saving the form and check that it creates a new recipe in the database
        recipe = form.save()
        self.assertEqual(recipe.name, 'Test')
        self.assertEqual(recipe.ingredients, 'Ing1, ing2, ing3')
    
    def test_recipe_form_invalid(self):
        # Missing title (required field)
        form_data = {
            'ingredients': 'Flour, Sugar',
            'cooking_time': 5,
        }
        form = RecipeForm(data=form_data)
        
        # The form should not be valid because the title is required
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)  # Check that the 'title' field has an error

    def test_recipe_form_saves_to_db(self):
        form_data = {
            'name': 'Test',
            'ingredients': 'Ing1, ing2, ing3',
            'cooking_time': 5,
        }
        form = RecipeForm(data=form_data)
        
        self.assertTrue(form.is_valid())  # Ensure the form is valid
        
        # Save the form and check that it creates a new Recipe instance in the database
        recipe = form.save()
        self.assertEqual(Recipe.objects.count(), 1)  # One recipe should exist in the DB now
        self.assertEqual(Recipe.objects.get(id=recipe.id).name, 'Test')