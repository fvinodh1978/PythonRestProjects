from django.contrib import admin
from .models import TestCases
from .utils.id_generator import IDGenerator

admin.site.register(TestCases)
admin.site.register(IDGenerator)
