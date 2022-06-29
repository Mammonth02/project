from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from apps.cars.models import *
from apps.profile1.models import *
from django.forms import Textarea


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['text']

        widgets = {
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Напиши сообшение'
            })
        }

class ReviewsAddForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ['reliability', 'comfort', 'performance', 'exterior_styling', 'interior_design', 'value_for_the_money', 'text']
        widgets = {
            'reviews': forms.Textarea(attrs={'cols': 60, 'rows': 5})
        }

class OtvetyForm(forms.ModelForm):
    class Meta:
        model = Otvety
        fields = ['text']

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