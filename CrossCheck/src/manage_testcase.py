import json

from rest_framework.response import Response
from rest_framework import status
from CrossCheck.serializers import TestCasesSerializer
from CrossCheck.models import TestCase


def get_test_case_logic(criteria):
    try:
        # Filter the TestCase based on criteria
        test_case = TestCase.objects.filter(**criteria).first()
        return test_case
    except Exception as e:
        return None


def check_test_cases_existence_logic(test_cases):
    existing_test_cases = []
    non_existing_test_cases = []

    for tc in test_cases:
        criteria = {
            "name": tc.get("name"),
            "suite": tc.get("suite"),
            "module": tc.get("module")
        }
        # Filter the TestCase based on multiple criteria
        exists = TestCase.objects.filter(**criteria).exists()
        if exists:
            existing_test_cases.append(tc)
        else:
            non_existing_test_cases.append(tc)

    response_data = {
        "existing_test_cases": existing_test_cases,
        "non_existing_test_cases": non_existing_test_cases
    }
    return response_data


def add_test_case_logic(request_data):
    if isinstance(request_data, list):
        serializer = TestCasesSerializer(data=request_data, many=True)
    else:
        serializer = TestCasesSerializer(data=request_data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def update_test_case_logic1(test_case, update_data):
    try:
        # Update the TestCase with new data
        serializer = TestCasesSerializer(test_case, data=update_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def update_test_case_logic(test_cases):
    for tc in test_cases:
        criteria = {
            "name": tc.get("name"),
            "suite": tc.get("suite"),
            "module": tc.get("module")
        }

        # Get the data for update
        update_data = {
            "description": tc.get("description"),
            "type": tc.get("type"),
            "testprofile": tc.get("testprofile"),
            "updatedby": tc.get("updatedby")
        }

        # Filter the TestCase based on multiple criteria
        test_case = TestCase.objects.filter(**criteria).first()

        # Update the TestCase with new data
        serializer = TestCasesSerializer(test_case, data=update_data, partial=True)

        if serializer.is_valid():
            serializer.save()
    return Response(test_cases, status=status.HTTP_200_OK)
