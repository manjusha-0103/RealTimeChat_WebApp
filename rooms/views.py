from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
from .consumers import ChatConsumer

# Create your views here.
@login_required
def teams(request):
    rooms = Teams.objects.all()
    r = {}
    for room in rooms:
        print(room,"\n", room.members.all())
        r[room] = room.members.all()
    print("m",r)
    return render(request,'teams.html',{'rooms': r})


@login_required
def team(request, slug):
    # print(request.user)
    team = Teams.objects.get(slug=slug)
    members = team.members.all()  # Retrieve members correctly
    messages = Messages.objects.filter(room=team)[0:25]
    
    return render(request,'team.html',{'room':team, 'messages':messages})