from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import DetailView, ListView, FormView, CreateView
from django.contrib.auth import authenticate, login, logout
from .log_in import LogForm
from django.contrib import auth
from .models import CustomUserCreationForm


# Create your views here.
def home_view(request):
	return render(request, "home.html")

class Login(FormView):
    form_class = LogForm
    template_name = 'log_in.html'
    success_url ="/"
    def form_valid(self, form):
        print("ICI")
        form = LogForm(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            print(user)
            if user and user.is_active:
                auth.login(self.request, user)
                return redirect("/")
        print("ici")
        return redirect("/Login")

class Register(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "registration.html"
    success_url="/"
    #def get(self, request):
    #    user = self.form_class.save(self)
    #    print(user)
    #    auth.login(self.request, user)
    

    #def get(self,request): 
     #   return redirect('/')

class Logout(DetailView):
    def get(self,request): 
        auth.logout(request)
        return redirect('/')