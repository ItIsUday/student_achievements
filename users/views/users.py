from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, FormView
from users.models import Counselor, Student, User
from home.models import Achievement, Organization

from users.forms import AchievementForm


class SignUpView(TemplateView):
    template_name = 'users/registration/signup.html'


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    obj=User.objects.get(username=request.user.username)
    if obj.is_student:
        usrtype='Student'
        stud=Student.objects.get(user=obj)
        ach=stud.achievements.all()
        context={
            'name':obj.first_name+" "+obj.last_name,
            'USN':stud.usn,
            'coun_name':stud.counselor.id,
            'usr':usrtype,
            'ach':ach
        }
        return render(request,"users/studentview.html",context)

    elif obj.is_counselor:
        usrtype='Counselor'
        ach=Achievement.objects.all()
        stud=Student.objects.all()
        coun=Counselor.objects.get(user=obj)
        context={
            'name':obj.first_name+" "+obj.last_name,
            'id':coun.id,
            'usr':usrtype,
            'ach':ach,
            'stud':stud
        }
        print(coun.id)
        return render(request,"users/counselorview.html",context)

    else:
        usrtype='Admin'
        ach=Achievement.objects.all()

    context={
        'usr':usrtype,
    }

    return render(request,"users/user.html",context)


def logout_view(request):
    logout(request)
    return render(request,"users/login.html",{'message':'Logged out'})


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

def addachievement(request):
    form=AchievementForm()
    if request.method=='POST':
        print(form['title'])
        return HttpResponseRedirect(reverse("index"))

    # studs=Student.objects.all()
    # orgs=Organization.objects.all()
    context={
        # 'studs':studs,
        # 'orgs':orgs,
        'form':form
    }
    return render(request,'users/add_achievement.html',context)