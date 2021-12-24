from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.http.response import Http404, HttpResponse
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
        return student_view(request,user)

    elif user.is_counselor:
        return counselor_view(request,user)

    else:
        user_type = 'Admin'
        context = {
            'user': user_type,
        }
        return render(request, "users/user.html", context)


def logout_view(request):
    logout(request)
    return render(request, "users/logout.html",{'message':'Logged out Successfully!'})


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
    if request.user.is_authenticated is not True:
        return render(request, "users/logout.html",{'message':'You must be signed in to add new achievement'})

    if request.method == 'POST':
        form=AchievementForm(request.POST, request.FILES)
        if form.is_valid():
            ach_obj=form.save()
            holders=form.cleaned_data.get("holders")
            for h in holders:
                h.achievements.add(ach_obj)

            context = {
                'message':'New Achievement Added Successfully!',
                'form': form
            }
            return render(request,'users/add_achievement.html',context)
        else:
            return HttpResponse(form.errors)
    
    form = AchievementForm()
    context = {
        'form': form
    }
    return render(request, 'users/add_achievement.html', context)

def counselor_view(request,user_obj):
    achievements=Achievement.objects.all()
    counselor = Counselor.objects.get(user=user_obj)
    context={
        'name': user_obj.get_full_name(),
        'id': counselor.id,
        'user_type': 'Counselor',
    }

    if request.method == 'POST':
        usn=request.POST.get('usn','')
        year=request.POST.get('year','')
        type=request.POST.get('type','')
        organization=request.POST.get('organization','')
        sortby=request.POST.get('sortby','')
                
        if usn:
            student = Student.objects.filter(usn=usn)
            if student:
                student = Student.objects.filter(usn=usn)[0]
                achievements=achievements.filter(holders=student)
            else:
                achievements=achievements.filter(id='ach')
        
        if type:
            achievements=achievements.filter(type=type)
        
        if year:
            achievements=achievements.filter(academic_year=year)

        if organization:
            achievements=achievements.filter(organization=organization)

        if sortby:
            achievements=achievements.order_by(sortby)

        context['usn']=usn
        context['year']=year
        context['type']=type
        context['org']=organization
            
    links=[]
    for a in achievements:
        link='file://'+str(a.certificate.file)
        links.append(link)
    
    achievements_links=zip(achievements,links)
    context['achievements']=achievements
    context['achievements_links']=achievements_links

    return render(request, "users/counselor_view.html", context)

def student_view(request,user_obj):
    student = Student.objects.get(user=user_obj)
    achievements=student.achievements.all()
    links=[]
    for a in achievements:
        link='file://'+str(a.certificate.file)
        links.append(link)
    
    achievements_links=zip(achievements,links)
    context = {
        'name': user_obj.get_full_name(),
        'usn': student.usn,
        'counselor': student.counselor.id,
        'user_type': 'Student',
        'achievements': achievements,
        'achievements_links':achievements_links,
    }
    return render(request, "users/student_view.html", context)
