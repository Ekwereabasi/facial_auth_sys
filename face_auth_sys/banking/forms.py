from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Account, Transaction

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15,required=False )
    profile_picture = forms.ImageField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'profile_picture', 'password1', 'password2']

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        fields = ['username', 'password', 'profile_picture']


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['balance', 'account_type']


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'description', ]  # Add relevant fields


class FacialRecognitionForm(forms.Form):
    image = forms.ImageField(label='Upload Your Photo', required=True)



class CustomUserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'profile_picture']