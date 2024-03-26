from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail
from legaltech import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.contrib.auth import authenticate, login, logout
from accounts.tokens import generate_token
from accounts.models import Profile,LSP,Msg,Friend,Fileupload
from django.shortcuts import get_object_or_404
from . import views
from django.contrib import messages
from django.http import JsonResponse



def lsp_dashboard(request):
    chat_user=User.objects.all()
    user = get_object_or_404(User, username=request.user.username)
    print("e1")
    # Fetch the user profile based on the 'user' field in the Profile model
    user_profile = get_object_or_404(Profile, user=user)
    print("e1")
    # Fetch the LSP details based on the 'user' field in the LSP model
    lsp_user = get_object_or_404(LSP, user=user)
    print("e1")
    context = {
        'user': user,
        'user_profile': user_profile,
        'lsp_user': lsp_user,
        'chat_user':chat_user,
    }
    return render(request,'lsp/lsp_dashboard.html',context)


def lsp_profile(request,username):
    user = get_object_or_404(User, username=username)
    print("e1")
    # Fetch the user profile based on the 'user' field in the Profile model
    user_profile = get_object_or_404(Profile, user=user)
    print("e1")
    # Fetch the LSP details based on the 'user' field in the LSP model
    lsp_user = get_object_or_404(LSP, user=user)
    print("e1")
    context = {
        'user': user,
        'user_profile': user_profile,
        'lsp_user': lsp_user,
    }
    return render(request,'lsp/lsp_profile.html',context)


def lsp_chat_list(request):
    chat_user=User.objects.all()
    context={
        'chat_user':chat_user,
    }
    for i in chat_user:
        print(f"{i.username}")
    return render(request,'lsp/lsp_chat_list.html',context)


def lsp_chat_ui(request,username):
    return render(request,'lsp/lsp_chat_ui.html',{'friend':username})



def send(request):
    # if request.user.is_anonymous or request.user.is_active==False:
    #     return redirect('/accounts/login')
    if request.method == 'POST':
        sender=request.POST.get("username")
        receiver=request.POST.get("friend")
        message=request.POST.get("message")
        message=message.strip()
        if (message == "") or (request.user.username != sender):
            return redirect('/lsp/lsp_chat_ui/'+receiver)
       
        newmessage=Msg(sender=sender,receiver=receiver,message=message)
        newmessage.save()

        return HttpResponse("message sent")

    return redirect('/')

def getmessages(request,friend):
    # if request.user.is_anonymous or request.user.is_active==False:
    #     return redirect('/accounts/login')
    # if User.objects.filter(username=friend).exists()==False:
    #     return redirect('/')
    # if request.user.username==friend:
    #     return redirect('/')
    all_messages=Msg.objects.all().filter(sender=request.user).filter(receiver=friend)|Msg.objects.all().filter(sender=friend).filter(receiver=request.user)

    return JsonResponse({"messages":list(all_messages.values())})



def checkview(request):
    if request.method == 'POST':
        friendusername =request.POST.get("friendusername")
        if request.user.username==friendusername:
            return redirect('/')
        if User.objects.filter(username=friendusername).exists():
            return redirect('/lsp/lsp_chat_ui/'+friendusername)
        else:
            return redirect('/')
    
    return redirect('/')