from django.urls import path, re_path

from . import views

app_name = 'academics'

urlpatterns = [
    path('', views.sign_in, name='sign-in'),
    path('authenticate', views.user_authentication, name='authenticate'),
    path('home', views.admin_home, name='admin-home'),
    path('user', views.user_registration, name='user-registration'),
    re_path(r'^student/(?:(?P<roll_number>[0-9]\d+)/)?$', views.view_students, name='view-student'),
    path('user/add', views.add_user_profile, name='add-user-profile'),
    path('student/<int:student_id>/update', views.update_student, name='update-student')
]
