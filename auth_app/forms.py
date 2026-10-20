"""Define forms for creating and editing users in Django Admin."""

from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Create users with email, full name and validated passwords."""

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "fullname")


class CustomUserChangeForm(UserChangeForm):
    """Edit user details, account flags and permission assignments."""

    class Meta(UserChangeForm.Meta):
        model = User
        fields = (
            "email",
            "fullname",
            "password",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )