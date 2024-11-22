from django.db import models
from .utils.id_generator import generate_custom_id


class TestCases(models.Model):
    objects: models.Manager

    testCaseName = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    testSteps = models.CharField(max_length=100)
    scriptName = models.CharField(max_length=100, default='Unnamed')
    testProfile = models.CharField(max_length=100, default='Unnamed')
    createdBy = models.CharField(max_length=100)
    createdOn = models.CharField(max_length=100)
    updatedBy = models.CharField(max_length=100)
    updatedOn = models.CharField(max_length=100)

    def __str__(self):
        return self.testCaseName + ' ' + self.description


class Users(models.Model):
    objects: models.Manager

    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    createdOn = models.CharField(max_length=100)

    def __str__(self):
        return self.username + ' ' + self.email

class SysUsers(models.Model):
    objects: models.Manager

    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    def __str__(self):
        return self.username + ' ' + self.email



class TestCase(models.Model):
    objects: models.Manager
    id = models.CharField(max_length=15, primary_key=True, default=generate_custom_id, editable=False, unique=True)
    name = models.CharField(max_length=50)
    suite = models.CharField(max_length=50)
    module = models.CharField(max_length=50)
    description = models.TextField()
    type = models.CharField(max_length=50)
    testprofile = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    createdby = models.CharField(max_length=10)
    updatedby = models.CharField(max_length=10)

    class Meta:
        db_table = 'cc_testcase'

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_custom_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.suite + ' ' + self.name
