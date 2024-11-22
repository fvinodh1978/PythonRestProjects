"""
URL configuration for QualityMonitor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
import sys

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'CrossCheck')))

from django.contrib import admin
from django.urls import path
from CrossCheck import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signUp', views.sign_up),
    path('login', views.login),
    path('getTestStatus', views.get_test_status),
    path('getTestCases', views.get_test_cases),
    path('getTestCases/<int:id>', views.get_test_details),
    path('addTestCase', views.add_test_case),
    path('updateTestCase', views.update_test_case),
    # path('updateTestCase/<str:id>', views.update_test_cases),
    path('deleteTestCase/<str:id>', views.delete_test_cases),
    path('runTest', views.execute_test),
    path('api/fetch-output/', views.fetch_script_output, name='fetch_output'),
    path('api/terminate-script/', views.terminate_script, name='terminate_script'),
    path('api/discoverTests', views.discover_tests, name='discover_tests'),
    path('api/add_test_cases/', views.add_test_case, name='add_test_case')
]
