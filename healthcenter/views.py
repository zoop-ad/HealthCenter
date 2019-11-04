from django.shortcuts import render
# Create your views here.

def index(request):
    return render(request, 'healthcenter/signin.html')

def signin(request):
    print(request.POST['username'])
    print(request.POST['password'])
    return render(request, 'healthcenter/signin.html')