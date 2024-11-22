import json

from django.contrib.auth import authenticate
from django.db.migrations import serializer
from rest_framework_simplejwt.tokens import RefreshToken
import time

from src.manage_testcase import update_test_case_logic, add_test_case_logic, get_test_case_logic, \
    check_test_cases_existence_logic
from utils.test_utils import get_class_names
from .models import TestCases, Users, TestCase
from .serializers import TestCasesSerializer, ActiveUsersSerializer, UserLoginSerializer, AuthUserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from CrossCheck.utils.invokePytest import run_test
from django.http import StreamingHttpResponse
import subprocess
import pytest
import io
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../CrossCheck/utils')))

# import pytest_collect_tests
from .tests import conftest


# from django.http import StreamingHttpResponse
#
# def generate_stream():
#     # Your logic to generate the data stream
#     yield "data1\n"
#     yield "data2\n"
#     # ...
#
# def stream_data(request):
#     response = StreamingHttpResponse(generate_stream(), content_type="text/plain")
#     response['Content-Disposition'] = 'attachment; filename="stream.txt"'
#     return response

#Admin User : admin
#Password : MyAdminPassword

#Get the Testcase Status
@api_view(['POST'])
def sign_up(request):
    serializer = AuthUserSerializer(data=request.data)
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
    test_status = TestCase.objects.all()
    serializer = TestCasesSerializer(test_status, many=True)
    # return JsonResponse({"testcases": serializer.data}, safe=False)
    return JsonResponse(serializer.data, safe=False)


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


# API to create a Testcase
@api_view(['POST'])
def add_test_case(request):
    criteria = {
        "name": request.data.get("name"),
        "suite": request.data.get("suite"),
        "module": request.data.get("module")
    }
    # Check if Testcase Exists Already
    test_case = get_test_case_logic(criteria)
    if not test_case:
        return add_test_case_logic(request.data)
    else:
        # Data to update
        update_data = {
            "description": request.data.get("description"),
            "type": request.data.get("type"),
            "testprofile": request.data.get("testprofile"),
            "updatedby": request.data.get("updatedby")
        }

        response = update_test_case_logic(test_case, update_data)
        return response


@api_view(['PUT'])
def update_test_case(request):
    # Call the update_test_case_logic function
    response = update_test_case_logic(request.data)
    return response


@api_view(['PUT'])
def update_test_case1(request):
    # Criteria to find the test case to be updated
    criteria = {
        "name": request.data.get("name"),
        "suite": request.data.get("suite"),
        "module": request.data.get("module")
    }
    test_case = get_test_case_logic(criteria)

    if not test_case:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        # Data to update
        update_data = {
            "description": request.data.get("description"),
            "type": request.data.get("type"),
            "testprofile": request.data.get("testprofile"),
            "updatedby": request.data.get("updatedby")
        }

        # Call the update_test_case_logic function
        response = update_test_case_logic(test_case, update_data)
        return response


#Update a Testcase
@api_view(['DELETE'])
def delete_test_cases(request, id):
    try:
        test_case = TestCase.objects.filter(id=id).first()
        test_case.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response(status=status.HTTP_404_NOT_FOUND)


#Add a New Testcase
@api_view(['POST'])
def execute_test(request):
    serializer = TestCasesSerializer(data=request.data)
    print(request.data)
    if serializer.is_valid():
        test_result = run_test(serializer.data['testCaseName'])
        # test_result=generate_stream()

        # return Response({'tests': serializer.data['testCaseName']}, status=status.HTTP_200_OK)
        return Response({'tests': test_result}, status=status.HTTP_200_OK)


def generate_stream():
    # Your logic to generate the data stream
    yield "data1\n"
    # time.sleep(25)
    yield "data2\n"
    # ...


def stream_data(request):
    response = StreamingHttpResponse(generate_stream(), content_type="text/plain")
    response['Content-Disposition'] = 'attachment; filename="stream.txt"'
    return response


@csrf_exempt
def fetch_script_output1(request):
    # Run your script and capture the output
    result = subprocess.run(
        ['python', 'C:\\Users\\VinodhFrancis\\Personal\\Projects\\PythonRestProjects\\CrossCheck\\src\\SampleTest.py'],
        stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    return JsonResponse({'output': output})


# Store the subprocess globally (not recommended for production)
current_process = None


@csrf_exempt
def fetch_script_output(request):
    global current_process
    if current_process and current_process.poll() is None:
        # Process is still running, terminate it
        current_process.terminate()

    # Start a new subprocess
    current_process = subprocess.Popen(
        ['python', 'C:\\Users\\VinodhFrancis\\Personal\\Projects\\PythonRestProjects\\CrossCheck\\src\\SampleTest.py'],
        stdout=subprocess.PIPE
    )
    output, _ = current_process.communicate()
    output = output.decode('utf-8')
    return JsonResponse({'output': output})


@csrf_exempt
def terminate_script(request):
    global current_process
    if current_process and current_process.poll() is None:
        current_process.terminate()
        return JsonResponse({'status': 'terminated'})
    return JsonResponse({'status': 'no process running'})


@api_view(['POST'])
@csrf_exempt
def discover_tests(request):
    if request.method == 'POST':
        module = request.data.get('fileName')
        suites = get_class_names(os.path.splitext(module)[0])
        for suite in suites:
            suite_name = 'CrossCheck/tests/' + suite.get('module') + '.py::' + suite.get('suite')
            print(suite_name)
            os.environ['PY_COLLECT_TESTS'] = '1'
            # Run pytest
            # subprocess.run(['pytest', '--collect-tests', 'CrossCheck/tests/test_calculator.py::TestMe', '-sv'])
            subprocess.run(['pytest', '--collect-tests', suite_name, '-sv'])
            # pytest.main(['--collect-tests', '--disable-warnings'])

            # Read the collected tests from the file
            file_path = 'collected_tests.json'
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    collected_tests = json.load(f)
                os.remove(file_path)  # Clean up the file after reading
                # add_test_cases(collected_tests)

                # Invoke update_test_case_logic for adding non existing cases
                response = check_test_cases_existence_logic(collected_tests)
                existing_test_cases = response.get('existing_test_cases')
                update_test_case_logic(existing_test_cases)

                # Invoke add_test_case_logic for adding non existing cases
                non_existing_test_cases = response.get('non_existing_test_cases')
                response = add_test_case_logic(non_existing_test_cases)

                return response
            else:
                return JsonResponse({'error': 'Collected tests file not found'}, status=500)

            # Access the collected tests from the custom plugin
            # collected_tests = getattr(conftest.CollectTestsPlugin, 'collected_tests', '[]')
            # tests = json.loads(collected_tests)
            # tests = {"key": collected_tests}
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
