import pytest
import sys
import subprocess
from CrossCheck.src.calculator import (summation, subtraction, multiplication, division)


def run_test1(testcase):
    pytest_args = ["-k", "test_calculator.py"]
    retcode = pytest.main(pytest_args, plugins=[MyPlugin()])
    print(retcode)

def run_test(testcase):
    command = "pytest -k test_calculator.py"
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        print(result)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

class MyPlugin:
    def pytest_sessionfinish(self):
        print("*** test run reporting finishing")

# if __name__ == "__main__":
#     sys.exit(pytest.main(["-qq"], plugins=[MyPlugin()]))


# run_test()
