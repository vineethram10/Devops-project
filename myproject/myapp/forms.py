from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import MyUser
import datetime

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    name = forms.CharField(max_length=255)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput) 
    class Meta:
        model = MyUser
        fields = ['name', 'email', 'password1', 'password2']
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        if isinstance(dob, str):
            for fmt in ('%Y-%m-%d', '%d-%m-%Y'):
                try:
                    return datetime.strptime(dob, fmt).date()
                except ValueError:
                    continue
            raise forms.ValidationError('Invalid date format. Use YYYY-MM-DD or DD-MM-YYYY.')
        return dob

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
