from django.contrib.auth import authenticate
from rest_framework import serializers

from CrossCheck.models import TestCases, Users


class TestCasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCases
        fields = ['id', 'testCaseName', 'description', 'type']

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'email', 'password', 'createdOn']


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            # Authenticate the user
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
                # return user
                return data
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

