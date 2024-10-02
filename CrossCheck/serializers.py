from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User
from CrossCheck.models import TestCases, Users

class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class TestCasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCases
        fields = ['id', 'testCaseName', 'description', 'type']

class ActiveUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'email', 'password', 'createdOn']


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        print("Vinodh1")
        if username and password:
            # Authenticate the user
            print("Vinodh2")
            user = authenticate(username=username, password=password)
            if user:
                print("Vinodh3")
                if not user.is_active:
                    print("Vinodh4")
                    raise serializers.ValidationError("User account is disabled.")
                # return user
                return data
            else:
                print("Vinodh5")
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

