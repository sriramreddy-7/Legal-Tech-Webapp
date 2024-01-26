from django.shortcuts import render ,redirect
from django.http import HttpResponse ,JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from legaltech import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.contrib.auth import authenticate, login, logout
from accounts.tokens import generate_token
from accounts.models import Profile,LSP,Message
from django.shortcuts import get_object_or_404
# chat/views.py


# from django.contrib.auth.decorators import login_required
# from .models import Message, UserProfile



def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')

def service(request):
    return render(request,'service.html')

def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('home')
    else:
        return render(request,'activation_failed.html')
    

def affidavit(request):
    if request.method =="POST":
        return redirect('affdoc')
        # return render(request,'affdoc.html')
    return render(request,'affidavit.html')


def affdoc(request):
    return render(request,'affdoc.html')

def notary(request):
    if request.method =="POST":
        purpose = request.POST.get('purpose1')
        if purpose == "land":
            return redirect('landnot')
        if purpose == "house":
            return redirect('housenot')
        if purpose == "rental":
            return redirect('rentalnot')
        # return render(request,'affdoc.html')
    return render(request,'notary.html')

def landnot(request):
    return render(request,'landnot.html')

def housenot(request):
    return render(request,'housenot.html')

def rentalnot(request):
    return render(request,'rentalnot.html')


def notdoc(request):
    return render(request,'notdoc.html')

def agreement(request):
    if request.method == "POST":
        purpose = request.POST.get('purpose1')
        if purpose == "partnership":
            return redirect('partnership_doc')
        if purpose == "payment":
            return redirect('payment_doc')
        if purpose == "lease":
            return redirect('lease_doc')
        # return render(request,'affdoc.html')
    return render(request,'agreement.html')


def partnership_doc(request):
    return render(request,'partnership_doc.html')

def payment_doc(request):
    return render(request,'payment_doc.html')

def lease_doc(request):
    return render(request,'lease_doc.html')

def help(request):
    return render(request,'help.html')
    
