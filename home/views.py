import pathlib
from wsgiref.util import FileWrapper

from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render
from django.urls import reverse

from home.forms import AchievementForm, OrganizationForm
from .models import Achievement, Organization


def add_achievement(request):
    if request.user.is_authenticated is not True:
        return render(request, "users/logout.html", {'message': 'You must be signed in to add new achievement'})

    if request.method == 'POST':
        form = AchievementForm(request.POST, request.FILES)
        if form.is_valid():
            ach_obj = form.save()
            holders = form.cleaned_data.get("holders")
            for h in holders:
                h.achievements.add(ach_obj)

            context = {'message': 'New Achievement Added Successfully!'}
            return render(request, 'users/add_achievement.html', context)
        else:
            return HttpResponse(form.errors)

    form = AchievementForm()
    return render(request, 'users/add_achievement.html', {'form': form})


def edit_achievement(request):
    if request.POST.get('id', ''):
        id = request.POST.get('id', '')
        ach_obj = Achievement.objects.get(id=id)
        data = {
            'title': ach_obj.title,
            'type': ach_obj.type,
            'date': ach_obj.achievement_date,
            'academic_year': ach_obj.academic_year,
            'organization': ach_obj.organization,
            'certificate': ach_obj.certificate,
        }
        form = AchievementForm(initial=data)
        context = {
            'ach_id': ach_obj.id,
            'form': form,
        }
        return render(request, 'users/add_achievement.html', context)

    else:
        form = AchievementForm(request.POST, request.FILES)
        id = request.POST.get('ach_id', '')
        ach_obj = Achievement.objects.get(id=id)
        if form.is_valid():
            ach_obj.certificate = form.cleaned_data.get('certificate')
            save_achievement(request, ach_obj)
        else:
            # form.is_valid gives False if new certificate is not uploaded
            save_achievement(request, ach_obj)
        return HttpResponseRedirect(reverse("index"))


def save_achievement(request, ach_obj):
    ach_obj.title = request.POST.get('title', '')
    ach_obj.type = request.POST.get('type', '').capitalize()
    ach_obj.achievement_date = request.POST.get('date', '')
    ach_obj.academic_year = request.POST.get('academic_year', '')
    ach_obj.organization = Organization.objects.get(id=request.POST.get('organization', ''))
    ach_obj.save()


def add_org(request):
    id = 'org' + str(Organization.objects.count() + 1)
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            org_obj = Organization.objects.create(
                id=id,
                name=form.cleaned_data.get('name'),
                type=form.cleaned_data.get('type'),
            )
            org_obj.save()
            return HttpResponseRedirect(reverse('add_achievement'))
        else:
            return HttpResponse("<h2>Organization already present.</h2>")

    form = OrganizationForm()
    return render(request, 'users/add_organization.html', {'form': form, 'id': id})


def download_certificate(request):
    id = request.GET['achid']
    obj = Achievement.objects.get(id=id)
    path = obj.certificate.path
    ext = pathlib.Path(path).suffix
    file = f'{obj.title}_{obj.achievement_date}{ext}'

    with open(path, 'rb') as f:
        wrapper = FileWrapper(f)
        content_type = 'application/force-download'
        response = HttpResponse(wrapper, content_type=content_type)
        response['Content-Disposition'] = f'attachment;filename={file}'
        return response
