from django.db import models
import uuid
from users.models import Profile

# Create your models here.

class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    # null =True der db-Eintrag darf leer sein, blank = True, es ist erlaubt eine leere Form zu senden
    description = models.TextField(null=True, blank=True)

    # für die Pics
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")

    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)

    #many to many, bzeieht sich auf untere Tag-Klasse es ist in quotes, weil Tag-Klasse unten ist, wenn Tag weiter oben wäre, könnte man sie weglassen, so wie defer im Prinzip
    tags = models.ManyToManyField('Tag', blank=True)

    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)

    # auto_now_add erstellt jedes mal wenn das model_instance erstellt wird ein Timestamp
    created = models.DateTimeField(auto_now_add=True)

    # 16-Character mit Stirngs und Ints, unique, wir überschreiben id
    # Ist Primärschlüssel, unique, und kann nicht editiert werden vom User
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return f'{self.title} {self.description}'
    
# one to many
class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )

    # owner = 

    # on_delete = , was wollen wir machen, mit den DB-Kindern, wenn ein Project deleted wurde? SET_NULL, entfernt den eintrag nicht, aber alles wird genullt, also leer,
    # CASCADE löscht alle Reviews, wenn das Projekt gelöscht wurde
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


    def __str__(self):
        return self.value

# many to many, wird aber in Project verknüpft
class Tag(models.Model):
    name= models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name
    



# queries
# queryset = ModelName.objects.all() - gibt alle zurüc
# .get - gibt ein einzelnes Objekt zurück
# .filter() - gibt gefiltertet mehrere Objekte zurück
# .exclude() - alle außer, die die man angibt