from django.shortcuts import render ,redirect
# Create your views here.
def home(request):
    return render(request,'home.html')

def admin_base(request):
    try:
        return render(request,'admin_base.html')
    except:
        return render(request,'error-404.html')

def client_login(request):
    return render(request,'client_login.html')

def service(request):
    return render(request,'service.html')

def home2(request):
    return render(request,'home.html')

def notary(request):
    return render(request,'notary.html')
    
def affidavit(request):
    return render(request,'affidavit.html')

def Agreement(request):
    return render(request,'Agreement.html')

def help(request):
    return render(request,'help.html')

def notdoc(request):
    return render(request,'notdoc.html')

def affdoc(request):
    return render(request,'affdoc.html')

# def login(request):
#     return render(request,'login.html')

def lsp_base(request):
    return render(request,'lsp_base.html')

def lsp_dashboard(request):
    return render(request,'lsp_dashboard.html')