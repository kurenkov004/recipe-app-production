from django import forms  # type: ignore
from django.forms import ModelForm, TextInput, Textarea, NumberInput, FileInput #type:ignore
from .models import Recipe
from django.contrib.auth.forms import UserCreationForm #type:ignore
from django.contrib.auth.models import User #type:ignore

CHART_CHOICES = (("#1", "Bar chart"), ("#2", "Pie chart"), ("#3", "Line chart"))

DIFFICULTY_CHOICES = (
    ("", "Any difficulty"),
    ("Easy", "Easy"),
    ("Medium", "Medium"),
    ("Intermediate", "Intermediate"),
    ("Hard", "Hard"),
)


# class-based form, using Django form as parent class
class RecipeSearchForm(forms.Form):
    recipe_name = forms.CharField(
        required=False, label="Type recipe name", max_length=120
    )
    difficulty = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES, required=False, label="Select difficulty"
    )
    ingredient = forms.CharField(
        required=False, label="Type ingredient", max_length=120
    )

#class-based form for adding recipes
class RecipeForm(forms.ModelForm):
    # Custom field definition for the recipe image, making it optional and applying custom styling.
    pic = forms.ImageField(label='Picture', required=False, widget=forms.FileInput(attrs={'class': 'form-control picture-change'}))
    
    class Meta:
        model = Recipe # Specify the model to be used to generate this form.
        fields = ['name', 'ingredients', 'cooking_time', 'pic']
        # Define custom widgets for form fields, applying Bootstrap 'form-control' class for styling.
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'ingredients': TextInput(attrs={'class': 'form-control'}),
            'cooking_time': NumberInput(attrs={'class': 'form-control'}),
            'pic': FileInput(attrs={'class': 'form-control','id': 'pic_select'})
        }


#form for adding users
class ModUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Enter a valid email address')

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super(ModUserCreationForm, self).__init__(*args, **kwargs)

        #customize help texts
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = '*Your password must contain at least 8 characters.'
        self.fields['password2'].help_text = None

        # Removing help text for fields you want to remove it from
        self.fields['email'].help_text = None