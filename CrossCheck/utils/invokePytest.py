import pytest
import sys
from CrossCheck.src.calculator import (summation, subtraction, multiplication, division)


def run_test(testcase):
    pytest_args = ["-k", "test_calculator.py"]
    retcode = pytest.main(pytest_args, plugins=[MyPlugin()])
    print(retcode)


class MyPlugin:
    def pytest_sessionfinish(self):
        print("*** test run reporting finishing")

# if __name__ == "__main__":
#     sys.exit(pytest.main(["-qq"], plugins=[MyPlugin()]))


# run_test()
