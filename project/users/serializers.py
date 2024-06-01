
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from rest_framework.validators import UniqueValidator
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# ///////////////////////////////////////////////////////////////////////////////////


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2',
                  'email')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token

# ////////////////////////////////////////////////////////////////////////////////////


class UserSerializer(ModelSerializer):

    class Meta:

        model = User
        fields = ["email", "password"]

    # def create(self, validated_data):

    #     request = self.context.get("request")

    #     if request:
    #         username = request.data["email"]
    #         return User.create(username=username, **validated_data)

    #     return User.create(**validated_data)
