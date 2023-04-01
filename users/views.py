from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout # brauchne wir für login etc
from django.contrib.auth.decorators import login_required # einfach über jede View setzen, wo wir wollen, dass der User eingeloggt ist, um sie sehen zu können
from django.contrib.auth.models import User
from django.contrib import messages
# from django.db.models import Q # verschoben nach utils.py
# from django.contrib.auth.forms import UserCreationForm # ähnlich wie eine ModelForm
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm # statt UserCreationForm
from .models import Profile, Message
from .utils import searchProfiles, paginateProfiles


# man sollte es nicht login() nennen, weil wir bereits eine solche Funktion importieren
def loginUser(request):
    page = 'login'

    # Wenn der Nutzer bereits eingloggt ist, wird er weitegreleitet, sobald er manuell versucht auf /login zu gehn
    if request.user.is_authenticated:

        return redirect('profiles')

    if request.method == 'POST':
        # print(request.POST)
        username = request.POST['username'].lower() # username muss intern immer lowercase sein, damit sich das nicht überschneidet
        password = request.POST['password']

        # wir checken mit dem try, ob der User in der DB ist
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
            

        # authenticate stellt sicher, dass das Passwort den Username matcht, return entweder User-Instance oder None
        user = authenticate(request, username=username, password=password)

        # Wenn der User existiert (not None)
        if user is not None:
            # erstellt eine Session für den user in der DB, und fügt sie in die Cookies des Browser ein 
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        
        else:
            messages.error(request, 'Username or password is incorrect')
            
    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)

    # messages haben unterschiedliche tags, man kann in den templates über {{ message.tags }} auf sie zugreifen
    # unterschiedliche tags haben unterschiedliche Farben
    messages.info(request, 'User was logged out')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        # commit False, speichert es als temporäre instanz erstmal
        if form.is_valid():
             # wir holen also erst die Instanz
            user = form.save(commit=False)
            # und gehen dann sicher, dass der user lowercase ist 
            user.username = user.username.lower()
            # und dann speichern wir
            user.save()

            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('edit-account')
        
        else:
            messages.success(request, 'An error has occurred during registration')

    context = {'page':page, 'form': form }
    return render(request, 'users/login_register.html', context)

def profiles(request):
    # # Suche
    # search_query = ''

    # # checken ob irgendwas in der Suche eingegeben wurde und dann den leeren Stirng überschreiben
    # if request.GET.get('search_query'):
    #     search_query = request.GET.get('search_query')
    #     print('SEARCH:', search_query)

    # # iexact = nur eaxkte Übereinstimmung
    # skills = Skill.objects.filter(name__icontains=search_query)

    # # __icontains: i = not caring about case sensitivity, contains = enthält folgendne Begriff etc.
    # # distinct ist notwendig sonst kriegen wir Duplikate wegen Child-Objects bei __in
    # profiles = Profile.objects.distinct().filter(
    #     Q(name__icontains=search_query) |
    #     Q(short_intro__icontains=search_query) |
    #     Q(skill__in=skills)
        
    #     )  # __in = child object
    # verlagert nach utils.py

    # aus utils, selbst erstellt Funktion, braucht request (gibt ja auch zwei Werte zurück)
    profiles, search_query = searchProfiles(request)

    custom_range, profiles = paginateProfiles(request, profiles, 6)

    context = {
        'profiles': profiles, 
        "search_query": search_query,
        "custom_range": custom_range,
        
        }

    return render(request, 'users/profiles.html', context)

# pk ist aus urls.py, steht hier für id -> path('profile/<str:pk>/', etc..
def userProfile(request, pk):
    # get gibt uns ein einzelnes Objekt, was in diesem Fall die pk ist also user_ID
    profile = Profile.objects.get(id=pk)

    # child object von profile, schließt alle descriptions aus, die einen leeren String als Wert haben
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")

    context = {
        'profile':profile,
        'topSkills': topSkills,
        'otherSkills': otherSkills
        }
    
    return render(request, 'users/user-profile.html', context)


@login_required(login_url = 'login')
def userAccount(request):
    profile = request.user.profile

    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {
        'profile':profile,
        'skills': skills,
        'projects': projects
        }
    
    return render(request, 'users/account.html', context)

@login_required(login_url = 'login')
def editAccount(request):

    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {
        'form': form,
        'profile':profile,
    }

    return render(request, 'users/profile-form.html', context)

@login_required(login_url = 'login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            # commit=False gibt einem nur das Objekt zurück, anstatt gleich zu speichern
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added succesfully!')
            return redirect('account' )

    context = {
        'form': form,
    }
    return render(request, 'users/skill_form.html', context)


@login_required(login_url = 'login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            # wir wissen bereits, wer der owner ist, deswegen hier nichts
            form.save()
            messages.success(request, 'Skill was updated succesfully!')
            return redirect('account' )

    context = {
        'form': form,
    }
    return render(request, 'users/skill_form.html', context)


@login_required(login_url = 'login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted succesfully!')
        return redirect('account')
       

    context = {
        'object': skill,
    }

    return render(request, "delete_template.html", context)

@login_required(login_url = 'login')
def inbox(request):
    profile = request.user.profile
    # man sollte das nicht messages nennen, sonst gibts einen Konflikt
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()

    context = {
        'messageRequests': messageRequests, 
        'unreadCount': unreadCount,
    }
    return render(request, 'users/inbox.html', context)

@login_required(login_url = 'login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)

    # als read markieren nach dem ersten lesen
    if message.is_read == False:
        message.is_read = True
        message.save()

    context = {
        'message': message,
    }

    return render(request, 'users/message.html', context)

# später noch ändern, zur zeit kann jeder nachrichten senden
def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()

            messages.success(request, 'Your message was successfully sent.')

            return redirect('user-profile', pk=recipient.id)

    context = {
        'recipient': recipient,
        'form': form,
    }
    return render(request, 'users/message_form.html', context)