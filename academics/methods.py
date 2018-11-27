from .models import Student, Professor


def generate_user_type_instance(user, request):
    name = user.first_name + ' ' + user.last_name
    user_type = request.POST['type']
    if request.POST['type'] == 'student':
        instance = Student(student_name=name, sex=request.POST['sex'], batch=request.POST['batch'],
                           joining_date=request.POST['joining_date'], roll_number=request.POST['roll_number'],
                           user=user)
    elif request.POST['type'] == 'professor':
        instance = Professor(professor_name=name, sex=request.POST['sex'], joining_date=request.POST['joining_date'],
                             user=user)
    return instance, user_type
