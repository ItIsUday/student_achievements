from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, FormView

from home.models import Achievement
from users.forms import AchievementForm
from users.models import Counselor, Student, User


class SignUpView(TemplateView):
    template_name = 'users/registration/signup.html'


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    user = User.objects.get(username=request.user.username)
    if user.is_student:
        student = Student.objects.get(user=user)
        context = {
            'name': user.get_full_name(),
            'usn': student.usn,
            'counselor': student.counselor.id,
            'user_type': 'Student',
            'achievements': student.achievements.all()
        }
        return render(request, "users/student_view.html", context)

    elif user.is_counselor:
        counselor = Counselor.objects.get(user=user)
        context = {
            'name': user.get_full_name(),
            'id': counselor.id,
            'user_type': 'Counselor',
            'achievements': Achievement.objects.all(),
            'students': Student.objects.all()
        }
        return render(request, "users/counselor_view.html", context)

    else:
        user_type = 'Admin'
        achievements = Achievement.objects.all()

    context = {
        'user': user_type,
    }

    return render(request, "users/user.html", context)


def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {'message': 'Logged out'})


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return self.form_invalid(form)


def add_achievement(request):
    form = AchievementForm()
    if request.method == 'POST':
        print(form['title'])
        return HttpResponseRedirect(reverse("index"))

    # students = Student.objects.all()
    # organizations = Organization.objects.all()
    context = {
        # 'students': students,
        # 'organizations': organizations,
        'form': form
    }
    return render(request, 'users/add_achievement.html', context)
