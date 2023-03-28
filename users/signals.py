from django.contrib.auth.models import User # django Usermodel für 1-to-1
from .models import Profile


# post_save triggert ein Signal, jedes Mal wenn ein model gespeichert wurde
# post_delete, jedes Mal, wenn ein model gelöscht wurde
from django.db.models.signals import post_save, post_delete


# decorator, macht das selbe aber mit kürzere Syntax, 
from django.dispatch import receiver


# receiver für signal
# sender = model, das sendet
# instance = Instanz des models, das es triggert
# created = True oder False, ob das model/also der User zu den Models hinzugefügt wurde, also ob es einen neuen Eintrag in der DB gibt
# **kwargs = ist wohl immer hier drin


# decorator statt untere Funktionen
# @receiver(post_save, sender=Profile)
# def profileUpdated(sender, instance, created, **kwargs):
#     print('Profile saved!', sender)
#     print('Instance:', instance)
#     print('Created:', created)

# @receiver(post_delete, sender=Profile)
# def deleteUser(sender, instance, **kwargs):
#     print('Deleted User')

# die Funktion wird hier als Argument übergeben, als auch das model, das sendet
# haben wir auskommentiert, weil wir jetzt stattdessen die decorators verwenden

# post_save.connect(profileUpdated, sender=Profile)
# post_delete.connect(deleteUser, sender=Profile)



# Wir erzeugen damit jedesmal ein Profil wenn ein User erzeugt wird, die verbunden sind
# da oben ein OneToOne-Field zwischen Profile und User ist, wird das Profil automatishc gelöscht, wenn de ruser gelöscht wird
def createProfile(sender, instance, created, **kwargs):
   if created:
       user = instance
       profile = Profile.objects.create(
           user= user,
           username = user.username,
           email = user.email,
           name = user.first_name
       )

# edit 
def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user # one to one relation machts möglich, so wie request.user etc
    
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


# Wenn ein Admin ein Profil löscht, bleibt der User, deswegen hier die Funktion
# damit wird also auch der User ds Profils gelöscht, wenn das Profil gelöscht wird
def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()


post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)