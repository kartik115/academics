from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.urls import reverse
from .models import Student
from .forms import UserForm, StudentForm, ProfessorForm
from .methods import *


def sign_in(request):
    return render(request, 'academics/login.html')


def user_authentication(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        if 'error_message' in request.session:
            del request.session['error_message']
        # print(user.id)
        login(request, user)
        return HttpResponseRedirect(reverse('academics:admin-home'))
    else:
        request.session['error_message'] = 'login and password did not match'
        return HttpResponseRedirect(reverse('academics:sign-in'))


@login_required(login_url='/academics/')
def user_registration(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            instance, user_type = generate_user_type_instance(user, request)
            context = dict(instance=instance, user_type=user_type)
            return render(request, 'academics/create_user_profile.html', context)
        else:
            print(form.errors)
            return HttpResponseRedirect(reverse('academics:admin-home'))
    else:
        user_type = request.GET.get('type', 'student')
        context = dict(type=user_type)
        return render(request, 'academics/user_registeration.html', context)


@login_required(login_url='/academics/')
def view_students(request, roll_number=None):
    if roll_number is not None:
        s = Student.objects.filter(roll_number=roll_number).first()
        context = dict(student=s)
        return render(request, 'academics/update_student.html', context)
    students = Student.objects.values('roll_number', 'student_name', 'sex', 'batch', 'joining_date', 'user__email')
    print(request.user.groups.values_list('name', flat=True))
    template = loader.get_template('academics/view_students.html')
    context = {
        'students_list': students,
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/academics/')
def admin_home(request):
    print(request.user.is_authenticated)
    return render(request, 'academics/home.html')


@login_required(login_url='/academics/')
def add_user_profile(request):
    my_group = Group.objects.get(name=request.POST['type'])
    if request.POST['type'] == "student":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            my_group.user_set.add(student.user)
            print(student.student_name)
        else:
            raise Exception(form.errors)
        return HttpResponseRedirect(reverse('academics:view-student'))
    elif request.POST['type'] == "professor":
        form = ProfessorForm(request.POST)
        if form.is_valid():
            professor = form.save()
            my_group.user_set.add(professor.user)
            print(professor.professor_name)
        else:
            raise Exception(form.errors)
        return HttpResponseRedirect(reverse('academics:view-student'))


@login_required(login_url='/academics/')
def update_student(request, student_id):
    s = Student.objects.filter(pk=student_id).first()
    email = request.POST['email']
    s.email = email
    s.save()
    return HttpResponseRedirect(reverse('academics:view-student', args=()))
