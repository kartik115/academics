from django.db import models
from django.contrib.auth.models import User, Group
from datetime import datetime, timedelta

# Create your models here.
GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

SEMESTER_CHOICES = (
    ('I', 'Even'),
    ('II', 'Odd'),
    ('I-1', 'Winter Course'),
    ('II-1', 'Summer Course')
)


def year_choices():
    return [(str(r)+"-"+str(r+1), str(r)+"-"+str(r+1)) for r in range(1984, datetime.utcnow().year)]


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=50, blank=False, null=False)
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES)
    batch = models.IntegerField(default=datetime.utcnow().year)
    joining_date = models.DateField(null=True)
    roll_number = models.IntegerField(unique=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = "students"


class Professor(models.Model):
    id = models.AutoField(primary_key=True)
    professor_name = models.CharField(max_length=50, blank=False, null=False)
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES)
    joining_date = models.DateField(null=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False)

    class Meta:
        db_table = "professors"


class Course(models.Model):
    subject_name = models.CharField(max_length=200)
    subject_code = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "courses"


class AcademicSession(models.Model):
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
    session_year = models.CharField(max_length=10, choices=year_choices())
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "academic_session"
        unique_together = ('semester', 'session_year')
