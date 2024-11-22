import json
import sys
import os
import pytest

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils')))

import pytest_collect_tests


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
#

class CollectTestsPlugin:
    def pytest_collection_modifyitems(self, session, config, items):
        tests = []
        for item in items:  # Access the docstring and class name
            docstring = item.obj.__doc__ if hasattr(item.obj, '__doc__') else ""
            class_name = item.parent.cls.__name__ if hasattr(item.parent, 'cls') else ""
            module_name = item.parent.module.__name__ if hasattr(item.parent, 'module') else ""
            tests.append({
                "name": item.name,
                "nodeid": item.nodeid,
                "description": docstring.strip(),
                "suite": class_name,
                "module": module_name.split('.')[-1],
                "type":"Sanity",
                "testprofile":"SanityProfile",
                "createdby":"Sive",
                "updatedby":"SVinodh"
            })

        # tests = [{"name": item.name, "nodeid": item.nodeid, "docstring": item.obj.__doc__.strip()} for item in items]
        # Store the test list as a class variable
        with open('collected_tests.json', 'w') as f:
            json.dump(tests, f, indent=2)
        CollectTestsPlugin.collected_tests = json.dumps(tests, indent=2)
        print(CollectTestsPlugin.collected_tests)
        pytest.exit("Collected tests successfully", 0)
