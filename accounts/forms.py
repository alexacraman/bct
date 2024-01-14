from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ["username", "email"]

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ["username", "email"]
        exclude = ['password']


class CustomUserAuth(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']