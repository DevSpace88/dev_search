from django.db import models
import uuid #braucht man halt meistens für Userkram
from django.contrib.auth.models import User # django Usermodel für 1-to-1


# # post_save triggert ein Signal, jedes Mal wenn ein model gespeichert wurde
# # post_delete, jedes Mal, wenn ein model gelöscht wurde
# from django.db.models.signals import post_save, post_delete


# # decorator, macht das selbe aber mit kürzere Syntax, 
# from django.dispatch import receiver



class Profile(models.Model):
    # 1-to-1-Relationship mit User, null und blank sollten nur beim Testen true sein vermute ich
    # User wird gelöscht, wenn profile gelöscht wird (gibt django user, das wir mit profile class hier verknüpfen)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    # geht in static/images/profiles wenn User Bild hochlädt (Pillow muss installiert sein etc.)
    profile_image = models.ImageField(null=True, blank=True, upload_to='profiles/', default='profiles/user-default.png')

    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_instagram = models.CharField(max_length=200, blank=True, null=True)
    social_website = models.CharField(max_length=200, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


    def __str__(self):
        return str(self.user.username)

class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True,)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)



    def __str__(self):
        return str(self.name)
    

# # receiver für signal
# # sender = model, das sendet
# # instance = Instanz des models, das es triggert
# # created = True oder False, ob das model/also der User zu den Models hinzugefügt wurde, also ob es einen neuen Eintrag in der DB gibt
# # **kwargs = ist wohl immer hier drin


# # decorator statt untere Funktionen
# # @receiver(post_save, sender=Profile)
# # def profileUpdated(sender, instance, created, **kwargs):
# #     print('Profile saved!', sender)
# #     print('Instance:', instance)
# #     print('Created:', created)

# # @receiver(post_delete, sender=Profile)
# # def deleteUser(sender, instance, **kwargs):
# #     print('Deleted User')

# # die Funktion wird hier als Argument übergeben, als auch das model, das sendet
# # haben wir auskommentiert, weil wir jetzt stattdessen die decorators verwenden

# # post_save.connect(profileUpdated, sender=Profile)
# # post_delete.connect(deleteUser, sender=Profile)



# # Wir erzeugen damit jedesmal ein Profil wenn ein User erzeugt wird, die verbunden sind
# # da oben ein OneToOne-Field zwischen Profile und User ist, wird das Profil automatishc gelöscht, wenn de ruser gelöscht wird
# def createProfile(sender, instance, created, **kwargs):
#    if created:
#        user = instance
#        profile = Profile.objects.create(
#            user= user,
#            username = user.username,
#            email = user.email,
#            name = user.first_name
#        )

# # Wenn ein Admin ein Profil löscht, bleibt der User, deswegen hier die Funktion
# # damit wird also auch der User ds Profils gelöscht, wenn das Profil gelöscht wird
# def deleteUser(sender, instance, **kwargs):
#     user = instance.user
#     user.delete()


# post_save.connect(createProfile, sender=User)
# post_delete.connect(deleteUser, sender=Profile)


# haben den signal-Kram in eine eigene Datei namens signals.py verschoben


class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True) # the empfänger soll die Nachricht weiterhin sehen können, wenn der Sender sein Profil gelöscht hat, Form kann submitted werden ohne Sender
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages") # related_name connected die Profile
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.subject
    
    class Meta:
        ordering = ["is_read", '-created']
