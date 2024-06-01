from django.db import models


class TestCases(models.Model):
    testCaseName = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    testSteps = models.CharField(max_length=100)
    createdBy = models.CharField(max_length=100)
    createdOn = models.CharField(max_length=100)
    updatedBy = models.CharField(max_length=100)
    updatedOn = models.CharField(max_length=100)

    def __str__(self):
        return self.testCaseName + ' ' + self.description
