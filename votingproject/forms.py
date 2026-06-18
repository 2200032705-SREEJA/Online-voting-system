
from django import forms

# The User model is used here to create a form for the default django user model
# It is used to create the registration form and the edit profile form
from django.contrib.auth.models import User

class signupForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password', 'repeatpassword', 'email', 'phonenumber']
        widgets = {
            'password': forms.PasswordInput,
        }