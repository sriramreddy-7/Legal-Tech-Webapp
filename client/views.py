from django.shortcuts import render ,redirect
from django.http import HttpResponse
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
from accounts.models import Profile,LSP,Doubts
from django.shortcuts import get_object_or_404
from accounts import views




    
def client_dashboard(request):
    lsp_users = LSP.objects.filter(lsp_type='Lawyer')
    profiles = Profile.objects.filter(user__in=lsp_users.values('user'))
    user_det = User.objects.filter(pk__in=lsp_users.values('user'))

    # profiles_with_lsps = []

    # for i in range(len(lsp_users)):
    #     profiles_with_lsps.append({
    #         'user_det': user_det[i],
    #         'lsp_user': lsp_users[i],
    #         'profile': profiles[i],
    #     })

    context = {
        'lsp_users':lsp_users,
    }
    
    return render(request,'client/client_dashboard.html',context)

def client_lsp_view(request):
    # user_det=User.objects.all()
    # profile_user=Profile.objects.all()
    # lsp_users= LSP.objects.all()
    lsp_users = LSP.objects.filter(lsp_type='Lawyer')
    profiles = Profile.objects.filter(user__in=lsp_users.values('user'))
    user_det = User.objects.filter(pk__in=lsp_users.values('user'))

    # profiles_with_lsps = []

    # for i in range(len(lsp_users)):
    #     profiles_with_lsps.append({
    #         'user_det': user_det[i],
    #         'lsp_user': lsp_users[i],
    #         'profile': profiles[i],
    #     })

    context = {
        'lsp_users':lsp_users,
    }
    
    return render(request,'client/client_lsp_view.html',context)


def client_lsp_profile(request,username):
    user = get_object_or_404(User, username=username)
    print("e1")
    # Fetch the user profile based on the 'user' field in the Profile model
    user_profile = get_object_or_404(Profile, user=user)
    print("e2")
    # Fetch the LSP details based on the 'user' field in the LSP model
    lsp_user = get_object_or_404(LSP, user=user)
    print("e3")
    context = {
        'user': user,
        'user_profile': user_profile,
        'lsp_user': lsp_user,
    }
    print("e4")
    return render(request,'client/client_lsp_profile.html',context)



def client_contact(request):
    if request.method == 'POST':
        # Extract data from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        type_of_doubt = request.POST.get('type_of_doubt')
        message = request.POST.get('message')
        print(first_name)
        print(last_name)
        print(email)
        print(type_of_doubt)
        print(message)
        # Validate data if necessary

        # Save data to the database
        d=Doubts.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            type_of_doubt=type_of_doubt,
            message=message
        )
        d.save()
        return render(request,'client/client_contact.html')
    
    return render(request,'client/client_contact.html')