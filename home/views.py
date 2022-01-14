from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render
from django.urls import reverse

from home.forms import AchievementForm
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
        id = request.POST.get('ach_id', '')
        ach_obj = Achievement.objects.get(id=id)
        save_achievement(request, ach_obj)
        return HttpResponseRedirect(reverse("index"))


def save_achievement(request, ach_obj):
    ach_obj.title = request.POST.get('title', '')
    ach_obj.type = request.POST.get('type', '').capitalize()
    ach_obj.achievement_date = request.POST.get('date', '')
    ach_obj.academic_year = request.POST.get('academic_year', '')
    org_obj = Organization.objects.get(id=request.POST.get('organization', ''))
    ach_obj.organization = org_obj
    if request.POST.get('certificate', ''):
        ach_obj.certificate = request.POST.get('certificate', '')
    ach_obj.save()
