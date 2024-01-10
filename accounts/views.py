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
from accounts.models import Profile,LSP
from django.shortcuts import get_object_or_404
# from accounts.models Profile


# Create your views here.
def home(request):
    return render(request,'home.html')

# def admin_base(request):
#     try:
#         return render(request,'admin_base.html')
#     except:
#         return render(request,'error-404.html')

# def lsp_base(request):
#     return render(request,'lsp_base.html')


def client_login(request):
    return render(request,'client_login.html')

def service(request):
    return render(request,'service.html')

def home2(request):
    return render(request,'home.html')

def lsp_dashboard(request):
    return render(request,'lsp/lsp_dashboard.html')

def admin_dashboard(request):
    return render(request,'admin/admin_dashboard.html')





def user_registration(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # pass2 = request.POST.get('pass2')
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('user_registration')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('user_registration')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
        # Welcome Email
        subject = "Welcome law Desk Login!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to law Desk!! \nThank you for visiting our website.\nWe have also sent you a confirmation email, please confirm your email address. \n\nThanking You Team Law Desk!"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ Law Desk - Login!"
        message2 = render_to_string('email_confirmation.html',{
            'name': myuser.first_name,
            'domain': current_site.domain,
            # 'domain':'https://legal-tech-webapp-git-sriram-sriramreddy-7.vercel.app',
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser),
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()
        
        return redirect('user_login')
    
    return render(request,'client/client_registration.html')



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
        return redirect('user_login')
    else:
        return render(request,'activation_failed.html')
    
    
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # if username == 'lawyer':
            return redirect("lsp_dashboard")
            # elif username == 'admin':
            #     return redirect('admin_dashboard')
            # else:
            #     return render(request,'server/error-404.html')
                
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('client/user_login')

    return render(request,'client/user_login.html')


def users_list(request):
    # user_det=User.objects.all()
    # profile_user=Profile.objects.all()
    # lsp_users= LSP.objects.all()
    lsp_users = LSP.objects.filter(lsp_type='Lawyer')
    profiles = Profile.objects.filter(user__in=lsp_users.values('user'))
    user_det = User.objects.filter(pk__in=lsp_users.values('user'))

    profiles_with_lsps = []

    for i in range(len(lsp_users)):
        profiles_with_lsps.append({
            'user_det': user_det[i],
            'lsp_user': lsp_users[i],
            'profile': profiles[i],
        })

    context = {
        'profiles_with_lsps': profiles_with_lsps,
    }
    
    return render(request,'admin/users_list.html',context)
    
    # return render(request,'admin/users_list.html')


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')



def client_registration(request):
    if request.method == "POST":
       username = request.POST.get('username')
       fname = request.POST.get('fname')
       lname = request.POST.get('lname')
       email = request.POST.get('email')
       password = request.POST.get('password') 
       mnumber=request.POST.get('mnumber')
       dob=request.POST.get('dob')       
    #    gender=request.POST.get('gender')
       country=request.POST.get('country')
       state= request.POST.get('state')
       city= request.POST.get('city')
       zipcode=request.POST.get('zipcode')
       if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('client_registration')
       if User.objects.filter(email=email).exists():
           messages.error(request, "Email Already Registered!!")
           return redirect('client_registration')
       
       if not username.isalnum():
           messages.error(request, "Username must be Alpha-Numeric!!")
       
       myuser = User.objects.create_user(username=username, email=email, password=password)
       myuser.first_name = fname
       myuser.last_name = lname
       myuser.is_active = False
       myuser.save()
       
       profile_user=Profile.objects.create(
           user=myuser,
           phone_number=mnumber,
           date_of_birth=dob,
        #    gender=gender,
            age=7,
           country=country,
           state_province=state,
           address_line=city,
           zip_code=zipcode
           )
       profile_user.save()
       messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
        # Welcome Email
       subject = "Welcome law Desk Login!"
       message = "Hello " + myuser.first_name + "!! \n" + "Welcome to law Desk!! \nThank you for visiting our website.\nWe have also sent you a confirmation email, please confirm your email address. \n\nThanking You Team Law Desk!"        
       from_email = settings.EMAIL_HOST_USER
       to_list = [myuser.email]
       send_mail(subject, message, from_email, to_list, fail_silently=True)
       
       # Email Address Confirmation Email
       current_site = get_current_site(request)
       email_subject = "Confirm your Email @ Law Desk - Login!"
       message2 = render_to_string('email_confirmation.html',{
           'name': myuser.first_name,
           'domain': current_site.domain,
           # 'domain':'https://legal-tech-webapp-git-sriram-sriramreddy-7.vercel.app',
           'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
           'token': generate_token.make_token(myuser),
       })
       email = EmailMessage(
       email_subject,
       message2,
       settings.EMAIL_HOST_USER,
       [myuser.email],
       )
       email.fail_silently = True
       email.send()   
       return redirect('user_login')
    
    else:
        print("Iam in inside the Else Block")
        return render(request,'client/client_registration.html')
    
    
    
def lsp_registration(request):
    if request.method == "POST":
       username = request.POST.get('username')
       fname = request.POST.get('fname')
       lname = request.POST.get('lname')
       email = request.POST.get('email')
       password = request.POST.get('password') 
       mnumber=request.POST.get('mnumber')
       dob=request.POST.get('dob')       
    #    gender=request.POST.get('gender')
       country=request.POST.get('country')
       state= request.POST.get('state')
       city= request.POST.get('city')
       zipcode=request.POST.get('zipcode')
       lsp_type=request.POST.get('lsp_type')
       display_picture=request.FILES.get('display_picture')
       signature=request.FILES.get('signature')
       enrollment_number=request.POST.get('enrollment_number')
       enrollment_year =request.POST.get('enrollment_year')
       bcpc=request.FILES.get('bcpc')
       university_name=request.POST.get('university_name')
       llb_passout_year=request.POST.get('llb_passout_year')
      
       if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('client_registration')
       if User.objects.filter(email=email).exists():
           messages.error(request, "Email Already Registered!!")
           return redirect('client_registration')
       
       if not username.isalnum():
           messages.error(request, "Username must be Alpha-Numeric!!")
       
       myuser = User.objects.create_user(username=username, email=email, password=password)
       myuser.first_name = fname
       myuser.last_name = lname
       myuser.is_active = False
       myuser.save()
       
       profile_user=Profile.objects.create(
           user=myuser,
           phone_number=mnumber,
           date_of_birth=dob,
        #    gender=gender,
            age=7,
           country=country,
           state_province=state,
           address_line=city,
           zip_code=zipcode
           )
       profile_user.save()
       
       lsp_user=LSP.objects.create(
           user=myuser,
           lsp_type=lsp_type,
           display_picture=display_picture,
           signature=signature,
           enrollment_number=enrollment_number,
           bar_council_practicing_certificate=bcpc,
           enrollment_year=enrollment_year,
           university_llb_completed=university_name,
           llb_passout_year=llb_passout_year,
       )
       lsp_user.save()
       
       messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
        # Welcome Email
       subject = "Welcome law Desk Login!"
       message = "Hello " + myuser.first_name + "!! \n" + "Welcome to law Desk!! \nThank you for visiting our website.\nWe have also sent you a confirmation email, please confirm your email address. \n\nThanking You Team Law Desk!"        
       from_email = settings.EMAIL_HOST_USER
       to_list = [myuser.email]
       send_mail(subject, message, from_email, to_list, fail_silently=True)
       
       # Email Address Confirmation Email
       current_site = get_current_site(request)
       email_subject = "Confirm your Email @ Law Desk - Login!"
       message2 = render_to_string('email_confirmation.html',{
           'name': myuser.first_name,
           'domain': current_site.domain,
           # 'domain':'https://legal-tech-webapp-git-sriram-sriramreddy-7.vercel.app',
           'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
           'token': generate_token.make_token(myuser),
       })
       email = EmailMessage(
       email_subject,
       message2,
       settings.EMAIL_HOST_USER,
       [myuser.email],
       )
       email.fail_silently = True
       email.send()
       
    #    return HttpResponse("<h1 style='color:green'>LSP User is created !</h1>")
       
       return redirect('user_login')
   
    return render(request,'lsp/lsp_registration.html')





def admin_lsp_profile(request,username):
    # user = get_object_or_404(User, username=username)
    user = get_object_or_404(User, username=username)
    
    # Fetch the user profile based on the 'user' field in the Profile model
    user_profile = get_object_or_404(Profile, user=user)
    
    # Fetch the LSP details based on the 'user' field in the LSP model
    lsp_user = get_object_or_404(LSP, user=user)

    context = {
        'user': user,
        'user_profile': user_profile,
        'lsp_user': lsp_user,
    }

    return render(request, 'admin/admin_lsp_profile.html', context)
   