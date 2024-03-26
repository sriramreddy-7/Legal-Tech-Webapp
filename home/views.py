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
# import base64
# import openai
from accounts.models import Chat

from django.utils import timezone
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


# def room(request,friendusername):
#     # if request.user.is_anonymous or request.user.is_active==False:
#     #     return redirect('/accounts/login')
#     # if request.user.username == friendusername:
#     #     return redirect('/')
#     return render(request, 'chatapp/chat_ui.html',{'friend':friendusername})



# def checkview(request,friendusername):
#     # if request.user.is_anonymous or request.user.is_active==False:
#     #     return redirect('/accounts/login')
#     # if request.method == 'POST':
#     # friendusername =request.POST.get("friendusername")
#         # if request.user.username==friendusername:
#         #     return redirect('/')
#     if User.objects.filter(username=friendusername).exists():
#             return redirect('/room/'+friendusername)
#     else:
#         return redirect('/')


# def send(request):
#     # if request.user.is_anonymous or request.user.is_active==False:
#     #     return redirect('/accounts/login')
#     if request.method == 'POST':
#         sender=request.POST.get("username")
#         receiver=request.POST.get("friend")
#         message=request.POST.get("message")
#         message=message.strip()
#         if (message == "") or (request.user.username != sender):
#             return redirect('/room/'+receiver)
#         if sender==receiver:
#             return redirect('/')
#         newmessage=Msg(sender=sender,receiver=receiver,message=message)
#         newmessage.save()
#         return HttpResponse("message sent")
#     return redirect('/')

# import json

# from django.core.serializers import serialize

# # def getmessages(request,friend):
# #     all_messages=Msg.objects.all().filter(sender=request.user).filter(receiver=friend)|Msg.objects.all().filter(sender=friend).filter(receiver=request.user)
# # #     all_messages = Msg.objects.filter(sender=request.user, receiver=friend) | Msg.objects.filter(sender=friend, receiver=request.user)
# #     serialized_messages = serialize('json', all_messages, fields=('id', 'sender', 'receiver', 'message', 'file_status', 'file_name', 'date'))

# #     # Convert serialized data to a Python list
# #     messages_list = json.loads(serialized_messages)

# #     return JsonResponse({"messages": messages_list})


# def getmessages(request,friend):
#     all_messages=Msg.objects.all().filter(sender=request.user).filter(receiver=friend)|Msg.objects.all().filter(sender=friend).filter(receiver=request.user)
  
#     return JsonResponse({"messages":list(all_messages.values())})



# def friends(request):
#     # if request.user.is_anonymous or request.user.is_active==False:
#     #     return redirect('/accounts/login')
#     if request.method=='POST':
#         friend=request.POST.get('friendusername')
#         nickname=request.POST.get('friendnickname')
#         user=request.user.username
#         if friend==user:
#             return redirect('/friends')
#         if friend=="" or nickname=="":
#             return redirect('/friends')
#         if Friend.objects.filter(friend=friend).filter(user=user).exists():
#             return redirect('/friends')
#         if User.objects.filter(username=friend).exists()==False:
#             return redirect('/friends')
#         new_friend=Friend.objects.create(user=user, nickname=nickname,friend=friend)
#         new_friend.save()
    
#     unsorted_friends=Friend.objects.all().filter(user=request.user.username)
#     user_friends=sorted(list(unsorted_friends.values()),key=lambda k:k['nickname'].lower())
#     return render(request,'chat_friends_list.html',{"user_friends": user_friends})



# def removefriend(request):
#     # if request.user.is_anonymous or request.user.is_active==False:
#     #     return redirect('/accounts/login')
    
#     if request.method =='POST':
#         friend=request.POST.get('friendusername')
#         user=request.user.username
#         if Friend.objects.all().filter(friend=friend).filter(user=user).exists()==False:
#             return redirect('/friends')

#         remove_friend=Friend.objects.all().filter(friend=friend).filter(user=user)
#         remove_friend[0].delete()
#         return redirect('/friends')

#     return redirect('/friends')


# def uploadfiles(request, friend):
#     # if request.user.is_anonymous or request.user.is_active==False:
#     #     return redirect('/accounts/login')

#     if(request.method=='POST'):
#         sender= request.user.username
#         receiver=friend
#         if ('file' in request.FILES)==False:
#             return redirect('/room/'+friend)
#         file=request.FILES.get('file')
#         new_file=Fileupload(file=file)
#         new_file.save()

#         file_name=new_file.file.name
#         #file_name=file_name[15:len(file_name):1]

#         new_message=Msg(sender=sender,receiver=receiver,message=new_file.file.url,file_status=True,file_name=file_name)
#         new_message.save()
#     return HttpResponse('File uploaded successfully!')


# def chat_friends(request):
#     return render(request,'chat_friends.html')

# openai_api_key = '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'
# openai.api_key = openai_api_key
# def ask_openai(message):
#     # model = 'text-davinci-003'  # GPT-3.5 engine
#     model = "gpt-3.5-turbo-instruct"  # Define model here

#     response = openai.Completion.create(
#         engine=model,
#         prompt=message,
#         max_tokens=150,
#         temperature=0.7,
#     )

#     answer = response.choices[0].text.strip()
#     return answer

# import openai
# from django.conf import settings

# # openai.api_key = settings.OPENAI_API_KEY
# # openai.api_key='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'
# openai.api_key='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'
# 4 KEY
# openai.api_key='asst_WiasYcXVMbtI1NtPUfzzyVEq'


# def is_law_related(message):
#     # Add your logic here to determine if the message is related to law
#     law_keywords = ['law', 'legal', 'justice', 'court',
                    
#     ]
#     return any(keyword in message.lower() for keyword in law_keywords)
# import openai

# def ask_openai(message):
#     model = "gpt-3.5-turbo-instruct"
    
#     # Check if the message is law-related
#     if is_law_related(message):
#         # Add instructions for law-based questions without using keywords
#         instructions = "Provide detailed and accurate information on the legal aspects of the following:"
        
#         # Concatenate the instructions with the user's message
#         prompt = f"{instructions}\n\n{message}"
        
#         # Generate a response from the model
#         response = openai.Completion.create(
#             engine=model,
#             prompt=prompt,
#             max_tokens=150,
#             temperature=0.7,
#         )
        
#         # Extract and return the generated answer
#         answer = response.choices[0].text.strip()
#     else:
#         answer = "I'm sorry, I can only provide information on law-related topics."
        
#     return answer


# def ask_openai(message):
#     model = "gpt-3.5-turbo-instruct"
#     # print(openai.api_key)
#     # if is_law_related(message):
#     response = openai.Completion.create(
#             engine=model,
#             prompt=message,
#             max_tokens=150,
#             temperature=0.7,
#         )
#     answer = response.choices[0].text.strip()
    # else:
    #     answer = "I'm sorry, I can only provide information on law-related Topics."
        
    # response = openai.Completion.create(
    #         engine=model,
    #         prompt=message,
    #         max_tokens=150,
    #         temperature=0.7,
    #     )
    # answer = response.choices[0].text.strip()

    return answer

def chatbot(request):
    chats = Chat.objects.filter(user=request.user.id)
    chats="admin"
    # if request.method == 'POST':
    #     message = request.POST.get('message')
    #     response = ask_openai(message)
    #     admin_user = User.objects.get(username='admin')
    #     chat = Chat(user=admin_user, message=message, response=response, created_at=timezone.now())
    #     chat.save()
    #     return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot/chatbot.html', {'chats': chats})
    # return render(request, 'chatbot/chatbot.html')



def home_chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        admin_user = User.objects.get(username='admin')
        chat = Chat(user=admin_user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request,'chatbot/home_chatbot.html')



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
    
def about(request):
    return render(request,'about.html')