# Generated by Django 5.0.6 on 2024-09-22 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestCases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testCaseName', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('testSteps', models.CharField(max_length=100)),
                ('createdBy', models.CharField(max_length=100)),
                ('createdOn', models.CharField(max_length=100)),
                ('updatedBy', models.CharField(max_length=100)),
                ('updatedOn', models.CharField(max_length=100)),
            ],
        ),
    ]
