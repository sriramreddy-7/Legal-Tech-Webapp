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

from django.contrib.auth import authenticate
from django.contrib.auth import logout,login
from accounts.models import Friend,Msg,Fileupload
from django.http import JsonResponse
# chat/views.py


# from django.contrib.auth.decorators import login_required
# from .models import Message, UserProfile


def home(request):
    return render(request,'home.html')

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
        messages.success(request, "Your Account has been Activated!!")
        return redirect('home')
    else:
        return render(request,'activation_failed.html')
  
  
def homechat(request):
    return render(request, 'home.html')


def chat_users_list(request):
    user = get_object_or_404(User, username=request.user.username)
    user_profile = get_object_or_404(Profile, user=user)
    if user_profile.is_service_provider:
        user_det = User.objects.filter(profile__is_client=True)
        context={
        # 'user_profile':user_profile,
        # 'lsp_user':lsp_user,
        'user_det':user_det,
        }
        return render(request, 'chatapp/chat_users_list.html',context)
    elif user_profile.is_client:
        user_det=User.objects.filter(profile__is_service_provider=True)
        context={
        # 'user_profile':user_profile,
        'user_det':user_det,
        # 'client_user':client_user,
        }
        return render(request, 'chatapp/chat_users_list.html',context)
    else:
        return HttpResponse("Data Base Error")
    # lsp_user=Profile.objects.filter(is_service_provider=True)
    # client_user=Profile.objects.filter(is_client=True)
    # context={
    #     'user_profile':user_profile,
    #     'lsp_user':lsp_user,
    #     'client_user':client_user,
    # }
    # return render(request, 'chatapp/chat_users_list.html',context)


def room(request,friendusername):
    # if request.user.is_anonymous or request.user.is_active==False:
    #     return redirect('/accounts/login')
    # if request.user.username == friendusername:
    #     return redirect('/')
    return render(request, 'chatapp/chat_ui.html',{'friend':friendusername})



def checkview(request,friendusername):
    # if request.user.is_anonymous or request.user.is_active==False:
    #     return redirect('/accounts/login')
    # if request.method == 'POST':
    # friendusername =request.POST.get("friendusername")
        # if request.user.username==friendusername:
        #     return redirect('/')
    if User.objects.filter(username=friendusername).exists():
            return redirect('/room/'+friendusername)
    else:
        return redirect('/')


def send(request):
    # if request.user.is_anonymous or request.user.is_active==False:
    #     return redirect('/accounts/login')
    if request.method == 'POST':
        sender=request.POST.get("username")
        receiver=request.POST.get("friend")
        message=request.POST.get("message")
        message=message.strip()
        if (message == "") or (request.user.username != sender):
            return redirect('/room/'+receiver)
        if sender==receiver:
            return redirect('/')
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


def friends(request):
    # if request.user.is_anonymous or request.user.is_active==False:
    #     return redirect('/accounts/login')
    if request.method=='POST':
        friend=request.POST.get('friendusername')
        nickname=request.POST.get('friendnickname')
        user=request.user.username
        if friend==user:
            return redirect('/friends')
        if friend=="" or nickname=="":
            return redirect('/friends')
        if Friend.objects.filter(friend=friend).filter(user=user).exists():
            return redirect('/friends')
        if User.objects.filter(username=friend).exists()==False:
            return redirect('/friends')
        new_friend=Friend.objects.create(user=user, nickname=nickname,friend=friend)
        new_friend.save()
    
    unsorted_friends=Friend.objects.all().filter(user=request.user.username)
    user_friends=sorted(list(unsorted_friends.values()),key=lambda k:k['nickname'].lower())
    return render(request,'chat_friends_list.html',{"user_friends": user_friends})



def removefriend(request):
    # if request.user.is_anonymous or request.user.is_active==False:
    #     return redirect('/accounts/login')
    
    if request.method =='POST':
        friend=request.POST.get('friendusername')
        user=request.user.username
        if Friend.objects.all().filter(friend=friend).filter(user=user).exists()==False:
            return redirect('/friends')

        remove_friend=Friend.objects.all().filter(friend=friend).filter(user=user)
        remove_friend[0].delete()
        return redirect('/friends')

    return redirect('/friends')



def uploadfiles(request, friend):
    # if request.user.is_anonymous or request.user.is_active==False:
    #     return redirect('/accounts/login')

    if(request.method=='POST'):
        sender= request.user.username
        receiver=friend
        if ('file' in request.FILES)==False:
            return redirect('/room/'+friend)
        file=request.FILES.get('file')
        new_file=Fileupload(file=file)
        new_file.save()

        file_name=new_file.file.name
        #file_name=file_name[15:len(file_name):1]

        new_message=Msg(sender=sender,receiver=receiver,message=new_file.file.url,file_status=True,file_name=file_name)
        new_message.save()
    return HttpResponse('File uploaded successfully!')


def chat_friends(request):
    return render(request,'chat_friends.html')