from django.shortcuts import render, redirect
from models import User, Travel
from django.contrib import messages
from django.db.models import Count

# Create your views here.
def index(request):

    return render(request, 'exam/index.html')

def register(request):
    if request.method == "POST":
        user = User.objects.register(request.POST)
        if 'errors' in user:
            for error in user['errors']:
                messages.error(request, error)
            return redirect('/')
        if 'theuser' in user:
            request.session['theuser'] = user['theuser']
            request.session['userid'] = user['userid']
            return redirect('/travels') #where do we want to go on register

def login(request):
    if request.method == "POST":
        user = User.objects.login(request.POST)
        if 'errors' in user:
            for error in user['errors']:
                messages.error(request, error)
                return redirect('/')
        if 'theuser' in user:
            request.session['theuser'] = user['theuser']
            request.session['userid'] = user['userid']
            return redirect('/travels') #where do we want to go on login

def logout(request):
    del request.session['theuser']
    del request.session['userid']
    return redirect('/')  #return to index on logout

def travels(request):
    context={'travel' :Travel.objects.filter(user_id=request.session['userid']),
    'everyone' :Travel.objects.exclude(user_id=request.session['userid'])
    }
    return render(request, 'exam/travels.html', context)

def join(request, id):
    ### section to add another users travel to the current users
    travel = Travel.objects.join(id, request.session['userid'])
    return

def trip(request, id):
    context={'travel' :Travel.objects.get(id=id), 'user' :User.objects.filter(travel__id=id)}
    return render(request, 'exam/destination.html', context)

def add(request):
    return render(request, 'exam/add.html')

def addtravel(request):
    if request.method =='POST':
        travel = Travel.objects.add(request.POST, request.session['userid'])
        if 'errors' in travel:
            for error in travel['errors']:
                messages.error(request, error)
            return redirect('/add')

        return redirect('/travels')
