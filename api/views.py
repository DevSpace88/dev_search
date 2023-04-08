# from django.http import JsonResponse # wenn man es ohne rest_framework macht


from rest_framework.decorators import api_view
from rest_framework.response import Response

# wir müssen serializer und model importieren!
from .serializers import ProjectSerializer
from projects.models import Project


@api_view(['GET'])
def getRoutes(request):

    # wird in ein JS-Array mit Object umgewandelt (also JSON)
    routes = [
        {'GET': '/api/projects'},
        {'GET': '/api/projects/id'},
        {'POST': '/api/projects/id/vote'},

        # von django selbst
        {'POST': '/api/users/token'}, 
        {'POST': '/api/users/token/refresh'}, 
    ]
    # safe=False bedeutet wir können mehr als nur einen dict zurückgeben/zugreifen
    # return JsonResponse(routes, safe=False)


    return Response(routes)

# wir können bei den api_views auch mehr als eine request-Methode verwenden also bspw. @api_view(['GET', 'POST',])
@api_view(['GET'])
def getProjects(request):

    # dann müssen wir unsere models queryen:
    projects = Project.objects.all()

    # wir müssen jetzt aber die Daten serialisieren, zweites Argument, müssen wir angeben ob nur ein Objekt oder viele, bei einzelnem Objekt -> many = False
    serializer = ProjectSerializer(projects, many=True)

    # müssen .data anhängen, können wir auch an den Konstruktor dranhängen, wenn wir den nicht mehr anders verwenden

    return Response(serializer.data)



@api_view(['GET'])
def getProject(request, pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False)
  
    return Response(serializer.data)