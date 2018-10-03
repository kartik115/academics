from django.db import models
from django.contrib.auth.models import User, Group
from datetime import datetime, timedelta

# Create your models here.
GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )


def year_choices():
    return [(r, r) for r in range(1984, datetime.utcnow().year + 1)]


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=50, blank=False, null=False)
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES)
    batch = models.IntegerField(default=datetime.utcnow().year)
    joining_date = models.DateTimeField(null=True)
    roll_number = models.IntegerField(unique=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = "students"


class Professor(models.Model):
    id = models.AutoField(primary_key=True)
    professor_name = models.CharField(max_length=50, blank=False, null=False)
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES)
    joining_date = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = "professors"


class Course(models.Model):
    subject_name = models.CharField(max_length=200)
    subject_code = models.CharField(max_length=10)
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "courses"

