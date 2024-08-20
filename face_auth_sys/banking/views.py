
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Account, Transaction
from .forms import UserRegistrationForm, UserLoginForm, TransactionForm, AccountForm, FacialRecognitionForm, CustomUserProfileForm
from rest_framework import generics
from .serializers import UserSerializer, AccountSerializer, TransactionSerializer
from django.core.exceptions import ValidationError
from .utils import authenticate_user_with_facial_recognition  # Replace with your actual authentication logic
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.contrib import messages




# Register view remains unchanged

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Check if user was created successfully
            if user:
                try:
                    # Create an account for the user
                    account = Account.objects.create(user=user)
                except Exception as e:
                    # Handle exceptions and log errors
                    print(f"Error creating account: {e}")
                    # Optionally, you could add an error to the form or perform other error handling
                # Log in the user
                login(request, user)
                return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'banking/register.html', {'form': form})

def dashboard(request):
    print(f"User authenticated: {request.user.is_authenticated}")  # Check if user is authenticated
    print(f"Username: {request.user.username}")  # Print the username to ensure it's correct
    
    user = get_object_or_404(CustomUser, username=request.user.username)
    account = get_object_or_404(Account, user=user)
    transactions = account.transaction_set.all()

    print(f"Account found: {account}")  # Ensure the account is found

    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = AccountForm(instance=account)
    
    return render(request, 'banking/dashboard.html', {
        'account': account,
        'transactions': transactions,
        'form': form,
    })


class MyLoginView(LoginView):
    template_name = 'banking/login.html'
    success_url = 'dashboard'

    def form_invalid(self, form):
        """Custom form validation to handle invalid login attempts"""
        form.add_error(None, "Your login credentials are incorrect.")
        return self.render_to_response(self.get_context_data(form=form))


class UserListCreate(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class AccountDetail(generics.RetrieveUpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class TransactionListCreate(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

def facial_login(request):
    if request.method == 'POST':
        form = FacialRecognitionForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.cleaned_data['image']
            try:
                user = authenticate_user_with_facial_recognition(uploaded_image)
                if user:
                    login(request, user)
                    return redirect('dashboard')  # Ensure this matches your URL pattern name
            except ValidationError as e:
                form.add_error(None, str(e))
    else:
        form = FacialRecognitionForm()
    
    return render(request, 'banking/facial_login.html', {'form': form})


@login_required
def profile_view(request):
    user = request.user

    if request.method == 'POST':
        form = CustomUserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
    else:
        form = CustomUserProfileForm(instance=user)

    return render(request, 'banking/profile.html', {'form': form})