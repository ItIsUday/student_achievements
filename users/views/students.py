from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView

from home import views as home_views
from users.forms import StudentSignUpForm
from users.models import User, Student
from users.utils import zip_links


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = "users/registration/signup_form.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "student"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(reverse("index"))


def student_view(request, user_obj):
    if request.method == 'POST':
        return home_views.edit_achievement(request)

    student = Student.objects.get(user=user_obj)
    achievements = student.achievements.all()

    context = {
        'usn': student.usn,
        'counselor': student.counselor.id,
        'user_type': Student.type,
        'achievements': achievements,
        'achievements_links': zip_links(achievements),
    }
    return render(request, "users/student_view.html", context)
