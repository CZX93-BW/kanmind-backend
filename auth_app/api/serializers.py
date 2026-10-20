"""Validate authentication input and serialize user information."""

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers


User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """Validate registration data and create users securely."""

    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )
    repeated_password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    class Meta:
        model = User
        fields = (
            "fullname",
            "email",
            "password",
            "repeated_password",
        )

    def validate_email(self, value):
        """Normalize the email domain and reject an existing address."""
        email = User.objects.normalize_email(value)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "user with this email already exists."
            )
        return email

    def validate(self, attrs):
        """Require matching passwords that pass Django validation."""
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError(
                {"repeated_password": "Passwords do not match."}
            )
        user = User(email=attrs["email"], fullname=attrs["fullname"])
        try:
            validate_password(attrs["password"], user=user)
        except DjangoValidationError as error:
            raise serializers.ValidationError({"password": error.messages})
        return attrs

    def create(self, validated_data):
        """Remove password confirmation and delegate user creation."""
        validated_data.pop("repeated_password")
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    """Validate login credentials and provide the authenticated user."""

    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Authenticate credentials or raise a validation error."""
        user = authenticate(
            request=self.context.get("request"),
            email=attrs["email"],
            password=attrs["password"],
        )
        if user is None:
            raise serializers.ValidationError("Invalid email or password.")
        attrs["user"] = user
        return attrs


class EmailCheckSerializer(serializers.Serializer):
    """Require a valid email address for a user lookup."""

    email = serializers.EmailField()


class UserSerializer(serializers.ModelSerializer):
    """Expose read-only user IDs, email addresses and full names."""

    class Meta:
        model = User
        fields = ("id", "email", "fullname")
        read_only_fields = ("id", "email", "fullname")