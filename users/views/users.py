from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, FormView
from nltk.metrics.distance import edit_distance

from home import views as home_views
from home.models import Achievement, Organization
from users.models import Counselor, Student, User


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


def counselor_view(request, user_obj):
    achievements = Achievement.objects.all()
    counselor = Counselor.objects.get(user=user_obj)
    context = {
        'name': counselor,
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

    context.update({'achievements': achievements, "achievements_links": zip_links(achievements)})

    return render(request, "users/counselor_view.html", context)


def student_view(request, user_obj):
    if request.method == 'POST':
        return home_views.edit_achievement(request)

    student = Student.objects.get(user=user_obj)
    achievements = student.achievements.all()

    context = {
        'name': student,
        'usn': student.usn,
        'counselor': student.counselor.id,
        'user_type': Student.type,
        'achievements': achievements,
        'achievements_links': zip_links(achievements),
    }
    return render(request, "users/student_view.html", context)


def get_suggestions(key, word):
    corpus = []
    if key == 'type':
        corpus = list(Achievement.objects.values_list('type', flat=True).distinct())
    elif key == 'organization':
        corpus = list(Organization.objects.values_list('name', flat=True).distinct())

    mn = 10
    distances = []
    for cor in corpus:
        ed = edit_distance(word, cor)
        mn = min(mn, ed)
        distances.append(ed)

    suggestions = []
    cor_ed = zip(corpus, distances)
    for cor, ed in cor_ed:
        if ed == mn:
            suggestions.append(cor)

    return suggestions


def zip_links(achievements):
    links = [f"download?achid={achievement.id}" for achievement in achievements]
    return zip(achievements, links)


def usn_complete(request):
    if 'term' in request.GET:
        qs = Student.objects.filter(usn__icontains=request.GET.get('term')).order_by('usn')
        usn_list = list(qs.values_list('usn', flat=True))
        return JsonResponse(usn_list, safe=False)
    return JsonResponse(None)


def type_complete(request):
    if 'term' in request.GET:
        qs = Achievement.objects.filter(type__icontains=request.GET.get('term'))
        type_list = list(qs.values_list('type', flat=True).distinct())
        return JsonResponse(type_list, safe=False)
    return JsonResponse(None)
