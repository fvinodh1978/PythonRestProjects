import inspect
import importlib
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../tests')))


def get_class_names(module_name):
    # Import the module
    module = importlib.import_module(module_name)
    # Get a list of all the members of the module
    members = inspect.getmembers(module, inspect.isclass)
    # Filter out classes that are not part of the module
    class_names = [{"suite": name, "module": module_name} for name, obj in members if obj.__module__ == module_name]
    return class_names


if __name__ == "__main__":
    # Replace 'your_module' with the actual module name
    module_name = 'test_operations'
    classes = get_class_names(module_name)
    print(f"Classes in module '{module_name}': {classes}")
