from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView

from users.forms import CounselorSignUpForm
from users.models import User


class CounselorSignUpView(CreateView):
    model = User
    form_class = CounselorSignUpForm
    template_name = "users/registration/signup_form.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "Counselor"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(redirect("index"))
