from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db import IntegrityError, models, router, transaction
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from core.settings import EMAIL_HOST_USER


# Create your views here.

def index(request):
    return render(request, "home.html")

def signup(request):
    if request.method == "POST" :
        #username = response.POST["username"]
        email = request.POST["email"]
        photo = request.FILES.get("image")
        phone = request.POST["phone"]
        password1 = request.POST["password"]
        try:  
            username = email.split('@')[0]  
            myuser = User.objects.create_user(email=email, username=username, photo=photo,phone=phone, password=password1)        
            myuser.save()
            #if myuser.objects.filter :
            '''if len(username) >10:
                messages.error(response,"Username should contain at most 10 characters.")'''
            
            messages.success(request,"You have successfully registered.")
            subject = "tweetme.com||Success of registration"
            message = f"""This mail is from tweetme.com.
You have successfully registered yourself with gmail account {email}.
HAVE NICE DAY!!! :)
                """
            # send_mail(subject,message,EMAIL_HOST_USER,[email])
        except IntegrityError:
            pass
        
        return redirect('signin')
      
    return render(request, "signup.html")

def signin(request):
    if request.method == "POST" :
        email  = request.POST.get('email')
        password = request.POST.get('password')
        username = email.split('@')[0]  
        print(username)
        _user = authenticate(username = username ,password = password)
        print(_user)
        if _user is not None :
            login(request,_user)
            messages.success(request,"You have logged in successfully .......")
            return redirect('home')
        else :
            messages.error(request,"Wrong credentials")    
            return redirect('login')
    
    return render(request, "signin.html")

@login_required
def profile(request):
    return render(request,'profile.html')

def contactView(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        if name and message and email and subject:
            subject = f'Let\'s ChatMeet.com || {subject}'
            message = f'''{message}\n\n\nUser Contact :\nFrom {name}\nEmail Address : {email}'''
            try:
               print(send_mail(subject=subject,message=message,from_email=email,recipient_list=[EMAIL_HOST_USER]))
            except BadHeaderError:
                return HttpResponse(BadHeaderError)
            return redirect('/')
    return render(request,'base.html')