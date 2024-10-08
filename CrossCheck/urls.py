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
from django.contrib import admin
from django.urls import path
from CrossCheck import views

#Admin User : admin
#Password : MyAdminPassword

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signUp', views.sign_up),
    path('login', views.login),
    path('getTestStatus', views.get_test_status),
    path('getTestCases', views.get_test_cases),
    path('getTestCases/<int:id>', views.get_test_details),
    path('addTestCase', views.add_test_cases),
    path('updateTestCase/<int:id>', views.update_test_cases),
    path('deleteTestCase/<int:id>', views.delete_test_cases),
    path('runTest', views.execute_test)
]
