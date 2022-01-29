from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, FormView

from users.models import User
from users.views.counselors import counselor_view
from users.views.students import student_view


class SignUpView(TemplateView):
    template_name = 'users/registration/signup.html'


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    user = User.objects.get(username=request.user.username)
    if user.is_student:
        return student_view(request, user)

    elif user.is_counselor:
        return counselor_view(request, user)

    else:
        return render(request, "users/user.html", {'user_type': 'Admin'})


def logout_view(request):
    logout(request)
    return render(request, "users/logout.html", {'message': 'Logged out Successfully!'})


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
