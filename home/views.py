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
    

def chat_page(request):
    return render(request, 'chat.html')


def get_messages(request):
    messages = Message.objects.all().order_by('-timestamp')[:10]
    data = {'messages': [{'user': msg.user_profile.user.username, 'content': msg.content, 'timestamp': msg.timestamp} for msg in messages]}
    return JsonResponse(data)


def post_message(request):
    user_profile = User.objects.get(user=request.user)
    content = request.POST.get('content')
    Message.objects.create(user_profile=user_profile, content=content)
    return JsonResponse({'status': 'ok'})
