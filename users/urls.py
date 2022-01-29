from django.urls import path

import users.utils as utils
from home import views as home_view
from users.views import counselors as counselor_view, students as student_view, users as user_view

urlpatterns = [
    path("", user_view.index, name="index"),
    path("login", user_view.LoginView.as_view(), name="login"),
    path("logout", user_view.logout_view, name="logout"),
    path("signup", user_view.SignUpView.as_view(), name="signup"),
    path("signup/student/", student_view.StudentSignUpView.as_view(), name="student_signup"),
    path('signup/counselor/', counselor_view.CounselorSignUpView.as_view(), name="counselor_signup"),
    path('my-counselees/', counselor_view.my_counselees, name="my_counselees"),
    path('add-achievement/', home_view.add_achievement, name="add_achievement"),
    path('add-organization/', home_view.add_org, name="add_organization"),
    path('download', home_view.download_certificate, name="download_certificate"),
    path('usn_complete', utils.usn_complete, name="usn_complete"),
    path('type_complete', utils.achievement_type_complete, name="achievement_type_complete"),
    path('typecomplete1', utils.organization_type_complete, name="organization_type_complete"),
]
