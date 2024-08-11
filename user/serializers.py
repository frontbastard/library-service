from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(required=False)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "is_staff",
            "first_name",
            "last_name",
            "is_active",
        )
        read_only_fields = ("is_staff",)
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5,
                "style": {"input_type": "password"},
                "label": _("Password")
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        instance = kwargs.get("instance")

        if not instance:
            self.fields.pop("is_active", None)
        elif request and (
            not request.user.is_staff or request.user == instance
        ):
            self.fields.pop("is_active", None)

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, set the password correctly and return it"""

        request = self.context.get("request")

        # Ensure only admins can change the is_active status
        if "is_active" in validated_data:
            if not request.user.is_staff:
                raise serializers.ValidationError(
                    {
                        "is_active": _(
                            "You do not have permission to "
                            "change the active status."
                        )
                    }
                )

            # Prevent self-deactivation
            if instance == request.user and not validated_data["is_active"]:
                raise serializers.ValidationError(
                    {"is_active": _("You cannot deactivate your own account.")}
                )

        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class UserDetailSerializer(UserSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "is_staff",
            "first_name",
            "last_name",
            "is_active",
        )


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Email address"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"),
                email=email, password=password
            )

            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _("Must include 'username' and 'password'.")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs
