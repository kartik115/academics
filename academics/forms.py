from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.username = user.first_name.lower() + '.' + user.last_name.lower()
        user.set_password(self.cleaned_data["password"])
        user.save()
        return user


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ('student_name', 'sex', 'joining_date', 'batch', 'roll_number', 'user')


class ProfessorForm(ModelForm):
    class Meta:
        model = Professor
        fields = ('professor_name', 'sex', 'joining_date', 'user')
