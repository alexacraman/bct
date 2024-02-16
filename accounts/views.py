from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, update_session_auth_hash, authenticate, login
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .forms import UserCreationForm, CustomUserAuth, CustomUserChangeForm

# accounts/ login/ [name='login']
# accounts/ logout/ [name='logout']
# accounts/ password_change/ [name='password_change']
# accounts/ password_change/done/ [name='password_change_done']
# accounts/ password_reset/ [name='password_reset']
# accounts/ password_reset/done/ [name='password_reset_done']
# accounts/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/ reset/done/ [name='password_reset_complete']


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email    = form.cleaned_data.get('email')
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'Email is already taken. Please choose a different one.')
            elif CustomUser.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken. Please choose a different one.')
            else:
                form.save()
                messages.success(request, 'Account created successfully. You can now log in.')
                return redirect('accounts:login_view')
        else:
            messages.error(request, 'There were errors in the registration form.')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomUserAuth(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome, {username}!')
                return redirect('accounts:account-menu')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'There is an error')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home_page')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully')
            return redirect('accounts:account-menu')
        else:
            messages.error(request, 'Please correct the errors')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change_form.html', {'form': form})

@login_required
def account_view(request):
    return render(request, 'account/account_list.html', {})

def edit_account(request):
    pk = request.user.pk
    # user = CustomUser.objects.get(pk=request.user.pk)
    custom_user = get_object_or_404(CustomUser, pk=pk)
    form = CustomUserChangeForm(instance=custom_user)
    print(form)
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=custom_user)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            user_form = form.save(commit=False)
            user_form.username = username
            user_form.email = email
            user_form.save()
            messages.success(request, 'User Changed')
            return redirect('accounts:account-menu')
        else:
            messages.error(request, 'There was an error in the form')
    return render(request, 'account/account_edit.html', {'form': form})