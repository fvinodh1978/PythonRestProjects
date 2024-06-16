from django.db.migrations import serializer
from django.http import JsonResponse

from .models import TestCases
from .serializers import TestCasesSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from CrossCheck.utils.invokePytest import run_test


#Get the list of all the (testcases
@api_view(['GET'])
def get_test_cases(request):
    test_status = TestCases.objects.all()
    serializer = TestCasesSerializer(test_status, many=True)
    return JsonResponse({"testcases": serializer.data}, safe=False)


#Get the Details of a Testcase
@api_view(['GET'])
def get_test_details(request, id):
    try:
        testcase = TestCases.objects.get(pk=id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TestCasesSerializer(testcase)
    Response.AppendHeader("Access-Control-Allow-Origin", "*");
    return Response(serializer.data)


#Get the Testcase Status
@api_view(['GET'])
def get_test_status(request):
    test_status = TestCases.objects.all()
    serializer = TestCasesSerializer(test_status, many=True)
    return JsonResponse({"testcases": serializer.data}, safe=False)


#Add a New Testcase
@api_view(['POST'])
def add_test_cases(request):
    serializer = TestCasesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


#Update a Testcase
@api_view(['PUT'])
def update_test_cases(request, id):
    try:
        testcase = TestCases.objects.get(pk=id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TestCasesSerializer(testcase, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Update a Testcase
@api_view(['DELETE'])
def delete_test_cases(request, id):
    try:
        testcase = TestCases.objects.get(pk=id)
        testcase.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


#Add a New Testcase
@api_view(['POST'])
def execute_test(request):
    serializer = TestCasesSerializer(data=request.data)
    if serializer.is_valid():
        test_result=run_test(serializer.data['testCaseName'])
        #return Response({'tests': serializer.data['testCaseName']}, status=status.HTTP_200_OK)
        return Response({'tests': test_result}, status=status.HTTP_200_OK)
