from django.db import models


class Employee(models.Model):
    emp_id = models.IntegerField()
    name = models.CharField(max_length=20)
    salary = models.FloatField()
    company = models.CharField(max_length=20)
    address = models.TextField()
