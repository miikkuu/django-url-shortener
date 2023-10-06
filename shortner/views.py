from django.shortcuts import render, redirect
import uuid
from .models import Url, ShortenedURLHistory
from django.http import HttpResponse
from .forms import CreateUserForm
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    return render(request, 'index.html')

#Registration page.
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account was created')
            return redirect('login')
    context = {'form': form}
    return render(request, 'register.html', context)



#login page
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Incorrect Username or Password')

    context={}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def create(request):
    if request.method == 'POST':
        link = request.POST['link']
        uid = str(uuid.uuid4())[:5]
        new_url = Url(link=link,uuid=uid)
        new_url.save()
        if request.user.is_authenticated:
            history = ShortenedURLHistory()
            history.shortened_url = link
            history.user = request.user
            history.save()
        return HttpResponse(uid)

def go(request, pk=None):
    # Define a mapping of keywords to URLs
    keyword_mapping = {
        'register': 'register/',
        'login': 'login/',
        'admin' : 'admin/',
        'logout' : 'logout/',
    }

    #allows redirection to intended page when not using uuid
    if pk is None:
        return redirect('register')

    if pk in keyword_mapping:
        return redirect(keyword_mapping[pk])

    try:
        url_details = get_object_or_404(Url, uuid=pk)
        return redirect(url_details.link)
    except ObjectDoesNotExist:
        return HttpResponse("URL not found.")


def view_history(request):
    if request.user.is_authenticated:
        history = ShortenedURLHistory.objects.filter(user=request.user).order_by('-timestamp')
        context = {'history': history}
        return render(request, 'view_history.html', context)
    else:
        return render(request, 'login.html')
