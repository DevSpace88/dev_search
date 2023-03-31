from .models import Project, Tag
from django.db.models import Q

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateProjects(request, projects, results):


    # damit wir das querien können, ala http://127.0.0.1:8000/projects/?page=1
    page = request.GET.get('page')

    # results = 3 # 3 Ergebnisse per Seite/  # wir passen results in der view, weswegen dass dynamisch ist -> comment
    paginator = Paginator(projects, results) # querying


    try:
        projects = paginator.page(page)
    except PageNotAnInteger:    # wenn jemand keine Zahl eingibt als query
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages # gibt uns einfach die letzte Seite, wenn der User eine Zahl eingibt, die es nicht gibt
        projects = paginator.page(page)

    leftIndex = (int(page) -2) 

    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = (int(page) +3) # wie weit die buttons neben dem button für die aktuelle Seite gehen

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages +1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, projects


def searchProjects(request):

    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        print('SEARCH:', search_query)

    tags = Tag.objects.filter(
        name__icontains=search_query
    )

    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |# geht eine Ebene höher, gibt uns jeden Namen vom Owner der beinhaltet
        Q(tags__in=tags)

    )

    return projects, search_query