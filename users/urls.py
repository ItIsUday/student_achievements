from django.urls import path

from .views import counselors, students, users

urlpatterns = [
    path("", users.index, name="index"),
    path("login", users.LoginView.as_view(), name="login"),
    path("logout", users.logout_view, name="logout"),
    path("signup", users.SignUpView.as_view(), name="signup"),
    path("signup/student/", students.StudentSignUpView.as_view(), name="student_signup"),
    path('signup/counselor/', counselors.CounselorSignUpView.as_view(), name="counselor_signup"),
    path('add-achievement/', users.add_achievement, name="add_achievement")
]
