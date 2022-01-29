from django.db.models import Count
from django.http import JsonResponse
from nltk import edit_distance
from plotly import graph_objects as go

from home.models import Achievement, Organization
from users.models import Student


class Chart:

    @staticmethod
    def achievement_count_per_student():
        students = Student.objects.all().order_by("usn")
        labels = [str(student) for student in students]
        values = [student.achievements.count() for student in students]
        chart = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
        return chart.to_html()

    @staticmethod
    def achievement_count_per_year():
        achievements = Achievement.objects.values("academic_year").annotate(count=Count('academic_year'))
        labels = [achievement["academic_year"] for achievement in achievements]
        values = [achievement["count"] for achievement in achievements]
        chart = go.Figure(data=[go.Bar(x=labels, y=values)])
        chart.update_yaxes(title_text="Achievements Count", dtick=1)
        chart.update_xaxes(title_text="Academic Year", range=[2010, 2022], dtick=1)
        return chart.to_html()

    @staticmethod
    def achievement_count_per_type():
        achievements = Achievement.objects.values("type").annotate(count=Count("type"))
        labels = [achievement["type"] for achievement in achievements]
        values = [achievement["count"] for achievement in achievements]
        chart = go.Figure(data=[go.Pie(labels=labels, values=values, title="Achievements Types")])
        chart.update_traces(textposition='inside', textinfo='percent+label')
        return chart.to_html()

    @staticmethod
    def achievement_count_per_organization():
        achievements = Achievement.objects.values("organization").annotate(count=Count("organization"))
        labels = [organization["name"] for organization in Organization.objects.values("name")]
        values = [achievement["count"] for achievement in achievements]
        chart = go.Figure(data=[go.Pie(labels=labels, values=values, title="Awarding Organizations")])
        chart.update_traces(textposition='inside', textinfo='percent+label')
        return chart.to_html()


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


def achievement_type_complete(request):
    if 'term' in request.GET:
        qs = Achievement.objects.filter(type__icontains=request.GET.get('term'))
        type_list = list(qs.values_list('type', flat=True).distinct())
        return JsonResponse(type_list, safe=False)
    return JsonResponse(None)


def organization_type_complete(request):
    if 'term' in request.GET:
        qs = Organization.objects.filter(type__icontains=request.GET.get('term'))
        type_list = list(qs.values_list('type', flat=True).distinct())
        return JsonResponse(type_list, safe=False)
    return JsonResponse(None)
