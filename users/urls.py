from django.urls import path

from home import views as home_view
from .views import counselors, students, users

urlpatterns = [
    path("", users.index, name="index"),
    path("login", users.LoginView.as_view(), name="login"),
    path("logout", users.logout_view, name="logout"),
    path("signup", users.SignUpView.as_view(), name="signup"),
    path("signup/student/", students.StudentSignUpView.as_view(), name="student_signup"),
    path('signup/counselor/', counselors.CounselorSignUpView.as_view(), name="counselor_signup"),
    path('my-counselees/', users.my_counselees, name="my_counselees"),
    path('add-achievement/', home_view.add_achievement, name="add_achievement"),
    path('add-organization/', home_view.add_org, name="add_organization"),
    path('download', home_view.download_certificate, name="download_certificate"),
    path('usn_complete', users.usn_complete, name="usn_complete"),
    path('type_complete', users.achievement_type_complete, name="achievement_type_complete"),
    path('typecomplete1', users.organization_type_complete, name="organization_type_complete"),
]
