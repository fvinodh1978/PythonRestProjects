from django.contrib.auth import authenticate
from django.db.migrations import serializer
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken

from .models import TestCases, Users
from .serializers import TestCasesSerializer, UsersSerializer, UserLoginSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from CrossCheck.utils.invokePytest import run_test
from django.http import StreamingHttpResponse


#Get the Testcase Status
@api_view(['POST'])
def sign_up(request):
    serializer = UsersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    print(request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Get the list of all the testcases
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
    # Response.AppendHeader("Access-Control-Allow-Origin", "*");
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
        test_result = run_test(serializer.data['testCaseName'])
        #return Response({'tests': serializer.data['testCaseName']}, status=status.HTTP_200_OK)
        return Response({'tests': test_result}, status=status.HTTP_200_OK)


def generate_stream():
    # Your logic to generate the data stream
    yield "data1\n"
    yield "data2\n"
    # ...


def stream_data(request):
    response = StreamingHttpResponse(generate_stream(), content_type="text/plain")
    response['Content-Disposition'] = 'attachment; filename="stream.txt"'
    return response
