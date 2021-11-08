from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from crm_cubedots.model.account import Account


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']

class SignInForm(AuthenticationForm):
    class Meta:
        model = User


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email','password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email = email, password=password):
                raise forms.ValidationError('Please enter a correct Email and password \n Note that both fields may be case-sensitive.')    

class UserCreationForms(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = '__all__'


class UserChangeForms(UserChangeForm):
    class Meta(UserChangeForm):
        model = User
        fields = '__all__'        
            