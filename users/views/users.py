from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, FormView

from home.models import Achievement, Organization
from users.models import Counselor, Student, User
from home import views as homeview

from nltk.metrics.distance import edit_distance
type_corpus = list(Achievement.objects.values_list('type',flat=True).distinct())
org_corpus = list(Organization.objects.values_list('name',flat=True).distinct())


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

def counselor_view(request,user_obj):
    achievements=Achievement.objects.all()
    counselor = Counselor.objects.get(user=user_obj)
    context={
        'name': user_obj.get_full_name().capitalize(),
        'id': counselor.id,
        'user_type': 'Counselor',
    }

    if request.method == 'POST':
        usn=request.POST.get('usn','').upper()
        year=request.POST.get('year','')
        type=request.POST.get('type','').title()
        organization=request.POST.get('organization','').title()
        sortby=request.POST.get('sortby','')
        my_ments=request.POST.get('my_mentees','')
                
        if usn:
            student = Student.objects.filter(usn=usn)
            if student:
                student = Student.objects.filter(usn=usn)[0]
                achievements=achievements.filter(holders=student)
            else:
                achievements=achievements.filter(id='ach')

        elif my_ments:
            student = Student.objects.filter(counselor=counselor)
            if student:
                student = Student.objects.filter(counselor=counselor)[0]
                achievements=achievements.filter(holders=student)
            else:
                achievements=achievements.filter(id='ach')
        
        if type:
            achievements=achievements.filter(type=type)
            if len(achievements)==0:
                sugs=get_suggestions('type',type)
                if sugs:
                    context['type_suggestions']=sugs
        
        if year:
            achievements=achievements.filter(academic_year=year)

        if organization:
            org_obj=Organization.objects.filter(name=organization)
            if org_obj:
                org_obj=org_obj[0]
                achievements=achievements.filter(organization=org_obj)
            else:
                achievements=achievements.filter(organization='ach')
                sugs=get_suggestions('organization',organization)
                if sugs:
                    context['org_suggestions']=sugs

        if sortby:
            achievements=achievements.order_by(sortby)

        context['usn']=usn
        context['year']=year
        context['type']=type
        context['org']=organization
              
    context['achievements']=achievements
    context['achievements_links']=ziplinks(achievements)

    return render(request, "users/counselor_view.html", context)

def student_view(request,user_obj):
    if request.method == 'POST':
        return homeview.edit_achievement(request)

    student = Student.objects.get(user=user_obj)
    achievements=student.achievements.all()
    context = {
        'name': user_obj.get_full_name(),
        'usn': student.usn,
        'counselor': student.counselor.id,
        'user_type': 'Student',
        'achievements': achievements,
        'achievements_links':ziplinks(achievements),
    }
    return render(request, "users/student_view.html", context)

def get_suggestions(str,word):
    if str=='type':
        corpus=type_corpus
    elif str=='organization':
        corpus=org_corpus
    
    mn=10
    distances=[]
    for cor in corpus:
        ed=edit_distance(word,cor)
        mn=min(mn,ed)
        distances.append(ed)

    suggestions=[]
    cor_ed=zip(corpus,distances)
    for cor,ed in cor_ed:
        if ed==mn:
            suggestions.append(cor)

    return suggestions

def ziplinks(achievements):
    links=[]
    for a in achievements:
        link='download?achid='+a.id
        links.append(link)
    
    return zip(achievements,links)

def usncomplete(request):
    if 'term' in request.GET:
        qs=Student.objects.filter(usn__icontains=request.GET.get('term')).order_by('usn')
        usnlist=list(qs.values_list('usn',flat=True))
        return JsonResponse(usnlist,safe=False)
    return JsonResponse(None)

def typecomplete(request):
    if 'term' in request.GET:
        qs=Achievement.objects.filter(type__icontains=request.GET.get('term'))
        typelist=list(qs.values_list('type',flat=True).distinct())
        return JsonResponse(typelist,safe=False)
    return JsonResponse(None)