from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView

from home.models import Achievement, Organization
from users.forms import CounselorSignUpForm
from users.models import User, Counselor, Student
from users.utils import Chart, get_suggestions, zip_links


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
        return redirect(reverse("index"))


def counselor_view(request, user_obj):
    achievements = Achievement.objects.all()
    counselor = Counselor.objects.get(user=user_obj)
    context = {
        'id': counselor.id,
        'user_type': Counselor.type,
    }

    if request.method == 'POST':
        usn = request.POST.get('usn', '').upper()
        year = request.POST.get('year')
        achievement_type = request.POST.get('achievement_type', '').title()
        organization = request.POST.get('organization')
        order = request.POST.get('sort_by')
        counselees = request.POST.get('my_counselees')

        if usn:
            student = Student.objects.filter(usn=usn).first()
            achievements = achievements.filter(holders=student) if student else []
        elif counselees:
            students = Student.objects.filter(counselor=counselor)
            achievements = achievements.filter(holders__in=students) if students else []

        if achievement_type:
            achievements = achievements.filter(type=achievement_type)
            if not achievements.exists():
                context['type_suggestions'] = get_suggestions('type', achievement_type)

        achievements = achievements.filter(academic_year=year) if year else achievements

        if organization:
            org_obj = Organization.objects.filter(name=organization).first()
            achievements = achievements.filter(organization=org_obj)
            if not achievements.exists():
                context['org_suggestions'] = get_suggestions('organization', organization)

        achievements = achievements.order_by(order) if order else achievements

        context.update({'usn': usn, 'year': year, 'achievement_type': achievement_type, 'org': organization})

    chart = Chart.achievement_count_per_type()
    context.update({'achievements': achievements, "achievements_links": zip_links(achievements), "fig": chart})

    return render(request, "users/counselor_view.html", context)


def my_counselees(request):
    if not request.user.is_authenticated:
        return render(request, "users/logout.html", {'message': 'You must be signed in.'})
    if not User.objects.get(username=request.user.username).is_counselor:
        return render(request, "users/my_counselees.html",
                      {'message': 'Only Counselors are Authorized to this page.'})

    me = Counselor.objects.get(user=request.user)
    students = Student.objects.filter(counselor=me).order_by('usn')
    context = {
        'id': me.id,
        'students': students,
    }
    return render(request, "users/my_counselees.html", context)
