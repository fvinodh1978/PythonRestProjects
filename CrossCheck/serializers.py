from rest_framework import serializers

from CrossCheck.models import TestCases


class TestCasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCases
        fields = ['id', 'testCaseName', 'description', 'type']
