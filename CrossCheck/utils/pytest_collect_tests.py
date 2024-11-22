# import pytest
import json

import sys
import os

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

def pytest_addoption(parser):
    parser.addoption("--collect-tests", action="store_true", help="Collect test names")

def pytest_configure(config):
    if config.getoption("--collect-tests"):
        config.pluginmanager.register(CollectTestsPlugin(), "collect-tests-plugin")

# class CollectTestsPlugin:
#     def pytest_collection_modifyitems(self, session, config, items):
#         tests = [{"name": item.name, "nodeid": item.nodeid} for item in items]
#         print(json.dumps(tests, indent=2))
#         pytest.exit("Collected tests successfully", 0)

class CollectTestsPlugin:
    def pytest_collection_modifyitems(self, session, config, items):
        tests = [{"name": item.name, "nodeid": item.nodeid} for item in items]
        # Store the test list as a class variable

        CollectTestsPlugin.collected_tests = json.dumps(tests, indent=2)
        print(CollectTestsPlugin.collected_tests)
        pytest.exit("Collected tests successfully", 0)