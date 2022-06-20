from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from apps.cars.models import *
from django.contrib.auth import get_user_model


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class ReviewsAddForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['reliability', 'comfort', 'performance', 'exterior_styling', 'interior_design', 'value_for_the_money', 'reviews']
        widgets = {
            'reviews': forms.Textarea(attrs={'cols': 60, 'rows': 5})
        }
  
class AutolikeForm(forms.ModelForm):
    class Meta:
        model = Auto_like
        fields = []

class AddAutoForm(forms.ModelForm):
    class Meta:
        model = Auto
        fields = ['video_link','model', 'make', 'color', 'drive_type', 'transmission', 'сondition', 'year', 'mileage', 'fuel_type', 'engine_size', 'doors', 'cylinders', 'vin', 'image', 'prise', 'description', 'type_auto']

class AddAutoImagesForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['image', 'auto']