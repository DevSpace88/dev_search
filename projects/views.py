from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.db.models import Q
from .utils import searchProjects

from .models import Project, Tag
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required # einfach über jede View setzen, wo wir wollen, dass der User eingeloggt ist, um sie sehen zu können

# projectsList = [
#     {
#     'id':'1',
#     'title': 'Ecommerce Website',
#     'description': 'Fully functional ecommerce website',
#     },
#     {
#     'id':'2',
#     'title': 'SAAS Website',
#     'description': 'Fully functional SAAS website',
#     },
#     {
#     'id':'3',
#     'title': 'Porn Website',
#     'description': 'Fully functional porn website',
#     },
#     {
#     'id':'4',
#     'title': 'DarkWeb Website',
#     'description': 'Fully functional darkweb website',
#     },

# ]

# das hier sind views
def projects(request):
    # return HttpResponse("here are our products")

    # page = 'projects'
    # number = 2
    # context = {
    #     'projects': projects,
    # }

    # search_query = ''

    # if request.GET.get('search_query'):
    #     search_query = request.GET.get('search_query')
    #     print('SEARCH:', search_query)

    # tags = Tag.objects.filter(
    #     name__icontains=search_query
    # )

    # projects = Project.objects.distinct().filter(
    #     Q(title__icontains=search_query) |
    #     Q(description__icontains=search_query) |
    #     Q(owner__name__icontains=search_query) |# geht eine Ebene höher, gibt uns jeden Namen vom Owner der beinhaltet
    #     Q(tags__in=tags)

    # )

    projects, search_query = searchProjects(request)
    
    context = {
        'projects': projects,
        'search_query': search_query,
    }

    return render(request, 'projects/projects.html', context)



# pk is in url, könnte auch was anderes genannt werden
def project(request, pk):
    # return HttpResponse("here is a single product" + ' ' + str(pk))
    # context = {
    #     "pk": pk,
    # }

    # projectObj = None
    # for i in projectsList:
    #     if i['id'] == pk:
    #         projectObj = i

    projectObj = Project.objects.get(id=pk)
    # tags = projectObj.tags.all()
    # return render(request, 'projects/single-project.html', {'project': projectObj, 'tags': tags })
    return render(request, 'projects/single-project.html', {'project': projectObj})


# form view
# parameter beim decorator, ist die Adresse wo man umgeleitet wird, wenn man nicht eingeloggt ist
@login_required(login_url="login")
def createProject(request):
    # setting the currently logged in user
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
         # print(request.POST['description']) # da POST ein dictionary ist, können wir di eeinzelnen Schlüssel zugreifen
         # request.FILES, muss rein, wenn wir Bilder hochladen wollen, über die Form/ oder Dateien
        form = ProjectForm(request.POST, request.FILES)
       
        if form.is_valid():
            # vermute mal, wenn man es quasi umleiten will macht man commit = False)
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')

    context = { 'form': form }
    return render(request, "projects/project_form.html", context)

@login_required(login_url="login")
def updateProject(request, pk):
    # genau so wie bei create, setzen wir erst, dass das nur der user machne kann
    profile = request.user.profile
    project = profile.project_set.get(id=pk)

    # auskommentiert, weil wir das jetzt über user und profile machen, sonst kann jeder über die id rein
    # project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
         # print(request.POST['description']) # da POST ein dictionary ist, können wir di eeinzelnen Schlüssel zugreifen
         # auch hier muss request.FILES rien, wenn wir Bilder updaten wollen
        form = ProjectForm(request.POST, request.FILES, instance=project)
       
        if form.is_valid():
            form.save()
            return redirect('account')

    context = { 'form': form }
    return render(request, "projects/project_form.html", context)

@login_required(login_url="login")
def deleteProject(request, pk):
    # wie oben, wir holen das profil, damit nur ein eingeloggter user solche Actions machen kann
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    # project = Project.objects.get(id=pk)

    if request.method == 'POST':
        project.delete()
        return redirect('account')

    context = { 'object': project }
    return render(request, "delete_template.html", context)