from django import forms
from django.contrib.auth.models import User
from .models import Profile, Store, Product, Review

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'description', 'image']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['store', 'name', 'description', 'price', 'stock', 'image']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
